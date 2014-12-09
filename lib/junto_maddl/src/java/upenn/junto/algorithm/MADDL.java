package upenn.junto.algorithm;

import upenn.junto.graph.*;
import upenn.junto.util.MessagePrinter;
import upenn.junto.util.ProbUtil;
import upenn.junto.util.Constants;
import upenn.junto.eval.GraphEval;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Map.Entry;

import gnu.trove.TDoubleArrayList;
import gnu.trove.TObjectDoubleHashMap;
import gnu.trove.TObjectDoubleIterator;

public class MADDL {
	public static void Run(Graph g, LabelGraph lc, int maxIter,
						   String mode, double mu1, double mu2, double mu3,
						   double mu4, int keepTopKLabels,
						   boolean useBipartiteOptimization, 
						   boolean verbose, ArrayList resultList) {
		
		// class prior normalization
		// g.ClassPriorNormalization();
		
//		if (verbose) { 
//			System.out.println("after_iteration " + 0 + 
//					" objective: " + GetObjective(g, mode, mu1,mu2, mu3, mu4, lc) +
//					" precision: " + LabelProp.GetPrecision(g));
//		}

		for (int iter = 1; iter <= maxIter; ++iter) {
			System.out.println("Iteration: " + iter);
			
			long startTime = System.currentTimeMillis();

			HashMap<String, TObjectDoubleHashMap> newDist =
				new HashMap<String, TObjectDoubleHashMap>();
			Iterator<String> viter = g._vertices.keySet().iterator();
			
			boolean printLog = false;
			
			while (viter.hasNext()) {
				String vName = viter.next();
				Vertex v = g._vertices.get(vName);
//				if (v.GetName().IsDocNode()) {
//					printLog = true;
//				}
				
				// if not present already, create a new label score map
				// for the current hash map. otherwise, it is an error
				if (!newDist.containsKey(vName)) {
					newDist.put(vName, new TObjectDoubleHashMap());
				} else {
					MessagePrinter.PrintAndDie("Duplicate node found: " + vName);
				}
				
				// compute weighted neighborhood label distribution
				Object[] neighNames = v.GetNeighborNames();
				for (int ni = 0; ni < neighNames.length; ++ni) {
					String neighName = (String) neighNames[ni];
					Vertex neigh = g._vertices.get(neighName);

					double mult = -1;
					mult = (v.GetContinuationProbability() * v.GetNeighborWeight(neighName) +
						    neigh.GetContinuationProbability() * neigh.GetNeighborWeight(vName));
					assert (mult > 0);

					ProbUtil.AddScores(newDist.get(vName),
									mu2 * mult,
									neigh.GetEstimatedLabelScores());
				}
				
				if (printLog) {
					System.out.println("Before norm: " + v.GetName() + " " +
							ProbUtil.GetSum(newDist.get(vName)));
				}
				
				// normalization is needed only for the original Adsorption algorithm
				if (mode.equals("original")) {
					// after normalization, we have the weighted
					// neighborhood label distribution for the current node
					ProbUtil.Normalize(newDist.get(vName));
				}
				
				if (printLog) {
					System.out.println("before_inj: " + v.GetName() + " " +
							ProbUtil.GetSum(newDist.get(vName)));
				}
				
				// add injection probability
				ProbUtil.AddScores(newDist.get(vName),
								mu1 * v.GetInjectionProbability(),
								v.GetInjectedLabelScores());
				
				if (printLog) {
					System.out.println(iter + " after_inj " + v.GetName() + " " +
							ProbUtil.GetSum(newDist.get(vName)) + 
							" inj_prob: " + v.GetInjectionProbability());
				}
				
				// add dummy label distribution
				ProbUtil.AddScores(newDist.get(vName),
								   mu3 * v.GetTerminationProbability(),
								   Constants.GetDummyLabelDist());
				
				// add label dependency/covariance based scores
				ProbUtil.AddScores(newDist.get(vName),
								   lc,
								   mu4,
								   v.GetEstimatedLabelScores());
				
				if (printLog) {
					System.out.println(iter + " after_dummy " + v.GetName() + " " +
							ProbUtil.GetSum(newDist.get(vName)) + " term_prob: " + 
							v.GetTerminationProbability());
				}
				
				// keep only the top scoring k labels, this is particularly useful
				// when a large number of labels are involved.
				if (keepTopKLabels < Integer.MAX_VALUE) {
					ProbUtil.KeepTopScoringKeys(newDist.get(vName), keepTopKLabels);
					if (newDist.get(vName).size() > keepTopKLabels) {
						MessagePrinter.PrintAndDie("size mismatch: " +
									newDist.get(vName).size() + " " + keepTopKLabels);
					}
				}
				
				// normalize
				ProbUtil.DivScores(newDist.get(vName), 
						           v.GetNormalizationConstant(g, mu1, mu2, mu3), mu4, lc);
			}
			
			double deltaLabelDiff = 0;
			int totalColumnUpdates = 0;
			int totalEntityUpdates = 0;
		
			// update all vertices with new estimated label scores
			viter = g._vertices.keySet().iterator();
			while (viter.hasNext()) {
				String vName = viter.next();
				Vertex v = g._vertices.get(vName);
				
				// deltaLabelDiff += Utils.GetDifferenceNorm2Squarred(v.GetEstimatedLabelScores(), 1.0,
				//		   											newDist.get(vName), 1.0);
				// g.vertices_.get(vName).SetEstimatedLabelScores(newDist.get(vName));
				
				if (!useBipartiteOptimization) {
					deltaLabelDiff += ProbUtil.GetDifferenceNorm2Squarred(
							v.GetEstimatedLabelScores(), 1.0, newDist.get(vName), 1.0);
					v.SetEstimatedLabelScores(newDist.get(vName).clone());
				} else {
					MessagePrinter.PrintAndDie("Currently not implemented!");
				}				
			}
			
			long endTime = System.currentTimeMillis();
			
			// clear map
			newDist.clear();
			
			int totalNodes = g._vertices.size();
			double deltaLabelDiffPerNode = (1.0 * deltaLabelDiff) / totalNodes;

			TObjectDoubleHashMap res = new TObjectDoubleHashMap();
			res.put(Constants.GetMRRString(), GraphEval.GetAverageTestMRR(g));
			res.put(Constants.GetPrecisionString(), GraphEval.GetAccuracy(g));
			resultList.add(res);
			if (verbose) {
				System.out.println("after_iteration " + iter +
						" objective: " + GetObjective(g, mode, mu1, mu2, mu3, mu4, lc) +
						" accuracy: " + res.get(Constants.GetPrecisionString()) +
						" rmse: " + GraphEval.GetRMSE(g) +
						" time: " + (endTime - startTime) +
						" label_diff_per_node: " + deltaLabelDiffPerNode +
						" mrr_train: " + GraphEval.GetAverageTrainMRR(g) +
						" mrr_test: " + res.get(Constants.GetMRRString()) +
						" total_seed_reachable: " + "NULL" +
						" column_updates: " + totalColumnUpdates +
						" entity_updates: " + totalEntityUpdates + "\n");
			}
			
			if (false && deltaLabelDiffPerNode <= Constants.GetStoppingThreshold()) {
				if (useBipartiteOptimization) {
					if (iter > 1 && iter % 2 == 1) {
						MessagePrinter.Print("Convergence reached!!");
						break;
					}
				} else {
					MessagePrinter.Print("Convergence reached!!");
					break;
				}
			}
		}
		
		if (resultList.size() > 0) {
			TObjectDoubleHashMap res =
				(TObjectDoubleHashMap) resultList.get(resultList.size() - 1);
			MessagePrinter.Print(Constants.GetPrecisionString() + " " +
								res.get(Constants.GetPrecisionString()));
			MessagePrinter.Print(Constants.GetMRRString() + " " +
								res.get(Constants.GetMRRString()));
		}
	}
	
	private static double GetObjective(Graph g, String mode,
					double mu1, double mu2, double mu3, double mu4,
					LabelGraph lc) {
		double obj = 0;
		Iterator<String> viter = g._vertices.keySet().iterator();
		while (viter.hasNext()) {
			String vName = viter.next();
			Vertex v = g._vertices.get(vName);
			obj += GetObjective(g, v, mu1, mu2, mu3, mu4, lc);
		}
		return (obj);
	}
	
	private static double GetObjective(Graph g, Vertex v,
				double mu1, double mu2, double mu3, double mu4, LabelGraph lc) {
		double obj = 0;
		
		// difference with injected labels
		if (v.IsSeedNode()) {
			obj += mu1 * v.GetInjectionProbability() *
					ProbUtil.GetDifferenceNorm2Squarred(
							v.GetInjectedLabelScores(), 1,
							v.GetEstimatedLabelScores(), 1);
		}
		
		// difference with labels of neighbors
		Object[] neighborNames = v.GetNeighborNames();
		for (int i = 0; i < neighborNames.length; ++i) {
			obj += mu2 * v.GetNeighborWeight((String) neighborNames[i]) *
					ProbUtil.GetDifferenceNorm2Squarred(
							v.GetEstimatedLabelScores(), 1,
							g._vertices.get((String) neighborNames[i]).GetEstimatedLabelScores(), 1);
		}
		
		// difference with dummy labels
		obj += mu3 * ProbUtil.GetDifferenceNorm2Squarred(
						Constants.GetDummyLabelDist(), v.GetTerminationProbability(),
						v.GetEstimatedLabelScores(), 1);
		
		// cost due to label dependencies
		obj += mu4 * GetLabelCovarianceCost(v, lc);
		
		return (obj);
	}
	
	private static double GetLabelCovarianceCost(Vertex v, LabelGraph lc) {
		double sum = 0;
		Iterator<Entry<String,TObjectDoubleHashMap>> iter = lc.GetIterator();
		while (iter.hasNext()) {
			Entry<String,TObjectDoubleHashMap> e = iter.next();
			TObjectDoubleIterator iter2 = e.getValue().iterator();
			while (iter2.hasNext()) {
				iter2.advance();
				double diff = v.GetEstimatedLabelScore(e.getKey()) -
							v.GetEstimatedLabelScore((String) iter2.key());
				sum += iter2.value() * diff * diff;
			}
		}

		// Because of the symmetry of the label graph, label pairs
		// are counted twice, hence we take half of it.
		return (0.5 * sum);
	}

}
