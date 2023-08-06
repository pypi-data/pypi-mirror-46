from model_factories import Weka_SVM, Weka_DecisionTree, TensorFlow
from loggers import vprint
from GradientFeatureAuditor import GradientFeatureAuditor
from audit_reading import graph_audit, graph_audits, rank_audit_files, group_audit_ranks
from consistency_graph import graph_prediction_consistency
from measurements import get_conf_matrix, accuracy, BCR
from datetime import datetime
from data import load_data, load_from_file
import csv

class Auditor():
  def __init__(self):
    self.measurers = [accuracy, BCR]
    self.model_options = {}
    self.verbose = True
    self.REPAIR_STEPS = 10
    self.RETRAIN_MODEL_PER_REPAIR = False
    self.WRITE_ORIGINAL_PREDICTIONS = True  
    self.ModelFactory = Weka_SVM
    self.kdd = False

  def __call__(self, data, output_dir=None, dump_all=False, features_to_audit=None):
    start_time = datetime.now()
  
    headers, train_set, test_set, response_header, features_to_ignore = data
  
    """
     ModelFactories require a `build` method that accepts some training data
     with which to train a brand new model. This `build` method should output
     a Model object that has a `test` method -- which, when given test data
     in the same format as the training data, yields a confusion table detailing
     the correct and incorrect predictions of the model.
    """
  
    all_data = train_set + test_set
    model_factory = self.ModelFactory(all_data, headers, response_header,
                                      features_to_ignore=features_to_ignore,
                                      options=self.model_options)
  
    if not self.RETRAIN_MODEL_PER_REPAIR:
      vprint("Training initial model.",self.verbose)
      model = model_factory.build(train_set)
  
      # Check the quality of the initial model on verbose runs.
      if self.verbose:
        print "Calculating original model statistics on test data:"
        print "\tTraining Set:"
        train_pred_tuples = model.test(train_set)
        train_conf_matrix = get_conf_matrix(train_pred_tuples)
        print "\t\tConf-Matrix:", train_conf_matrix
        for measurer in self.measurers:
          print "\t\t{}: {}".format(measurer.__name__, measurer(train_conf_matrix))
  
        print "\tTesting Set:"
        test_pred_tuples = model.test(test_set)
        test_conf_matrix = get_conf_matrix(test_pred_tuples)
        print "\t\tConf-Matrix", test_conf_matrix
        for measurer in self.measurers:
          print "\t\t{}: {}".format(measurer.__name__, measurer(test_conf_matrix))
  
  
      model_or_factory = model
    else:
      model_or_factory = model_factory
  
    # Translate the headers into indexes for the auditor.
    audit_indices_to_ignore = [headers.index(f) for f in features_to_ignore]

    # Don't audit the response feature.
    audit_indices_to_ignore.append(headers.index(response_header))

   # Prepare the auditor.
    auditor = GradientFeatureAuditor(model_or_factory, headers, train_set, test_set,
                                     repair_steps=self.REPAIR_STEPS, kdd=self.kdd,
                                     features_to_ignore=audit_indices_to_ignore,
                                     features_to_audit=features_to_audit,
                                     output_dir=output_dir,dump_all=dump_all)
  
    # Perform the Gradient Feature Audit and dump the audit results into files.
    audit_filenames = auditor.audit(verbose=self.verbose)
 
    ranked_features = []
    for measurer in self.measurers:
      vprint("Ranking audit files by {}.".format(measurer.__name__),self.verbose)
      ranked_graph_filename = "{}/{}.png".format(auditor.OUTPUT_DIR, measurer.__name__)
      graph_audits(audit_filenames, measurer, ranked_graph_filename)
      ranks = rank_audit_files(audit_filenames, measurer)
      vprint("\t{}".format(ranks), self.verbose)
      ranked_features.append( (measurer, ranks) )

    end_time = datetime.now()
    
    # Store a summary of this experiment.
    summary = [
      "Audit Start Time: {}\n".format(start_time),
      "Audit End Time: {}\n".format(end_time),
      "Retrained Per Repair: {}\n".format(self.RETRAIN_MODEL_PER_REPAIR),
      "Model Factory ID: {}\n".format(model_factory.factory_name),
      "Model Type: {}\n".format(model_factory.verbose_factory_name),
      "Non-standard Model Options: {}\n".format(self.model_options),
      "Train Size: {}\n".format(len(train_set)),
      "Test Size: {}\n".format(len(test_set)),
      "Non-standard Ignored Features: {}\n".format(features_to_ignore),
      "Features: {}\n\n".format(headers)]

    # Print summary 
    for line in summary:
      print(line) 

    for ranker, ranks in ranked_features:
      print("Ranked Features by {}: {}\n".format(ranker.__name__, ranks))
      groups = group_audit_ranks(audit_filenames, ranker)
      print("\tApprox. Trend Groups: {}\n".format(groups))

    # Dump all experiment results if opted  
    if dump_all:
      vprint("Dumping original training data.", self.verbose)
      # Dump the train data to the log.
      train_dump = "{}/original_train_data".format(auditor.OUTPUT_DIR)
      with open(train_dump + ".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in train_set:
          writer.writerow(row)
  
      if self.WRITE_ORIGINAL_PREDICTIONS:
        # Dump the predictions on the test data.
        with open(train_dump + ".predictions", "w") as f:
          writer = csv.writer(f)
          file_headers = ["Response", "Prediction"]
          writer.writerow(file_headers)
          for response, guess in train_pred_tuples:
            writer.writerow([response, guess])
  
      vprint("Dumping original testing data.", self.verbose)
      # Dump the train data to the log.
      test_dump = "{}/original_test_data".format(auditor.OUTPUT_DIR)
      with open(test_dump + ".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in test_set:
          writer.writerow(row)
  
      if self.WRITE_ORIGINAL_PREDICTIONS:
        # Dump the predictions on the test data.
        with open(test_dump + ".predictions", "w") as f:
          writer = csv.writer(f)
          file_headers = ["Response", "Prediction"]
          writer.writerow(file_headers)
          for response, guess in test_pred_tuples:
            writer.writerow([response, guess])
  
      # Graph ://github.com/algofairness/BlackBoxAuditing.gitthe audit files.
      vprint("Graphing audit files.",self.verbose)
      for audit_filename in audit_filenames:
        audit_image_filename = audit_filename + ".png"
        graph_audit(audit_filename, self.measurers, audit_image_filename)
 
      # Store a graph of how many predictions change as features are repaired.
      vprint("Graphing prediction changes throughout repair.",self.verbose)
      output_image = auditor.OUTPUT_DIR + "/similarity_to_original_predictions.png"
      graph_prediction_consistency(auditor.OUTPUT_DIR, output_image)
  
      # Store a summary of this experiment to file.
      summary_file = "{}/summary.txt".format(auditor.OUTPUT_DIR)
      with open(summary_file, "w") as f:
        for line in summary:
          f.write(line)
  
        for ranker, ranks in ranked_features:
          f.write("Ranked Features by {}: {}\n".format(ranker.__name__, ranks))
          groups = group_audit_ranks(audit_filenames, ranker)
          f.write("\tApprox. Trend Groups: {}\n".format(groups))
  
      vprint("Summary file written to: {}".format(summary_file), self.verbose)

def main():
  # format data
  data = load_data("german")

  # set the auditor
  auditor = Auditor()
  auditor.model = Weka_SVM

  # call the auditor
  auditor(data, output_dir="try", features_to_audit=["checking_status","duration"], dump_all=True)

if __name__=="__main__":
  main() 
