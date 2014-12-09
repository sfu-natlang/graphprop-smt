package upenn.junto.util;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Hashtable;
import java.util.Iterator;

import upenn.junto.type.ObjectDoublePair;
import upenn.junto.util.Constants;
import upenn.junto.util.MessagePrinter;

import gnu.trove.TObjectDoubleHashMap;
import gnu.trove.TObjectDoubleIterator;
import upenn.junto.graph.LabelGraph;

public class ProbUtil {
	
  public static TObjectDoubleHashMap GetUniformPrior(ArrayList<String> labels) {
    int totalLabels = labels.size();
    assert (totalLabels > 0);
    double prior = 1.0 / totalLabels;
    assert (prior > 0);

    TObjectDoubleHashMap retMap = new TObjectDoubleHashMap();
    for (int li = 0; li < totalLabels; ++li) {
      retMap.put(labels.get(li), prior);
    }
    return (retMap);
  }

  // this method returns result += mult * addDist
  public static void AddScores(TObjectDoubleHashMap result, double mult,
                               TObjectDoubleHashMap addDist) {
    assert (result != null);
    assert (addDist != null);

    TObjectDoubleIterator iter = addDist.iterator();
    while (iter.hasNext()) {
      iter.advance();
      double adjVal = mult * iter.value();
 
      result.adjustOrPutValue(iter.key(), adjVal, adjVal);
    }
  }
  
  public static void AddScores(TObjectDoubleHashMap result,
		                       LabelGraph lc, double mult, TObjectDoubleHashMap addDist) {
	  assert (lc != null);
	  assert (addDist != null);
	  assert (result != null);

	  TObjectDoubleIterator iter = addDist.iterator();
	  while (iter.hasNext()) {
		  iter.advance();
		  TObjectDoubleHashMap lv = lc.GetLabelCov((String) iter.key());
		  if (lv != null) {
			  TObjectDoubleIterator lvIter = lv.iterator();
			  while (lvIter.hasNext()) {
				  lvIter.advance();

				  // symmetry of the covariances used here.
				  // C_{ll'} x Y^{^}_{il'} = C_{l'l} x Y^{^}_{il'}
				  double adjVal = mult * lvIter.value() * iter.value();
				  result.adjustOrPutValue(lvIter.key(), adjVal, adjVal);
			  }
		  }
	  }
  }

  public static void DivScores(TObjectDoubleHashMap result, double divisor) {
    assert (result != null);
    assert (divisor > 0);

    TObjectDoubleIterator li = result.iterator();
    while (li.hasNext()) {
      li.advance();
      // System.out.println("Before: " + " " + li.key() + " " + li.value() + " " + divisor);
      double newVal = (1.0 * li.value()) / divisor;
      result.put(li.key(), newVal);
      // System.out.println("After: " + " " + li.key() + " " + result.get(li.key()) + " " + divisor);
    }
  }
  
	public static void DivScores(TObjectDoubleHashMap result, double divisor,
								 double mu4, LabelGraph lc) {
		assert (result != null);
		assert (lc != null);
		assert (divisor > 0);

		TObjectDoubleIterator li = result.iterator();
		while (li.hasNext()) {
			li.advance();

			double newVal = (1.0 * li.value())
					/ (divisor + mu4 * lc.GetLabelCovSum((String) li.key()));
			result.put(li.key(), newVal);
		}
	}
	
  public static void KeepTopScoringKeys(TObjectDoubleHashMap m, int keepTopK) {
    ArrayList<ObjectDoublePair> lsps = CollectionUtil.ReverseSortMap(m);

    // the array is sorted from large to small, so start
    // from beginning and retain only top scoring k keys.
    m.clear();
    int totalAdded = 0;
    int totalSorted = lsps.size();
    // for (int li = lsps.size() - 1; li >= 0 && totalAdded <= keepTopK; --li) {
    for (int li = 0; li < totalSorted && totalAdded < keepTopK; ++li) {
      ++totalAdded;

      if (lsps.get(li).GetScore() > 0) {
        m.put(lsps.get(li).GetLabel(), lsps.get(li).GetScore());
      }
    }
		
    // size of the new map is upper bounded by the max
    // number of entries requested
    assert (m.size() <= keepTopK);
  }

  public static void Normalize(TObjectDoubleHashMap m) {
    Normalize(m, Integer.MAX_VALUE);
  }

  public static void Normalize(TObjectDoubleHashMap m, int keepTopK) {
    // if the number of labels to retain are not the trivial
    // default value, then keep the top scoring k labels as requested
    if (keepTopK != Integer.MAX_VALUE) {
      KeepTopScoringKeys(m, keepTopK);
    }

    TObjectDoubleIterator mi = m.iterator();
    double denom = 0;
    while (mi.hasNext()) {
      mi.advance();
      denom += mi.value();
    }
    // assert (denom > 0);

    if (denom > 0) {
      mi = m.iterator();
      while (mi.hasNext()) {
        mi.advance();
        double newVal = mi.value() / denom;
        mi.setValue(newVal);
      }
    }
  }

  public static double GetSum(TObjectDoubleHashMap m) {
    TObjectDoubleIterator mi = m.iterator();
    double sum = 0;
    while (mi.hasNext()) {
      mi.advance();
      sum += mi.value();
    }
    return (sum);
  }

  public static double GetDifferenceNorm2Squarred(TObjectDoubleHashMap m1,
                                                  double m1Mult, TObjectDoubleHashMap m2, double m2Mult) {
    TObjectDoubleHashMap diffMap = new TObjectDoubleHashMap();

    // copy m1 into the difference map
    TObjectDoubleIterator iter = m1.iterator();
    while (iter.hasNext()) {
      iter.advance();
      diffMap.put(iter.key(), m1Mult * iter.value());
    }

    iter = m2.iterator();
    while (iter.hasNext()) {
      iter.advance();
      diffMap.adjustOrPutValue(iter.key(), -1 * m2Mult * iter.value(), -1
                               * m2Mult * iter.value());
    }

    double val = 0;
    iter = diffMap.iterator();
    while (iter.hasNext()) {
      iter.advance();
      val += iter.value() * iter.value();
    }

    return (Math.sqrt(val));
  }

  // KL (m1 || m2)
  public static double GetKLDifference(TObjectDoubleHashMap m1,
                                       TObjectDoubleHashMap m2) {
    double divergence = 0;

    TObjectDoubleIterator iter = m1.iterator();
    while (iter.hasNext()) {
      iter.advance();
      if (iter.value() > 0) {
        //				if (!m2.containsKey(iter.key()) && m2.get(iter.key()) <= 0) {
        //					divergence += Double.NEGATIVE_INFINITY;
        //				} else {
        // add a small quantity to the numerator and denominator to avoid
        // infinite divergence
        divergence += iter.value()
          * Math.log((iter.value() + Constants.GetSmallConstant())
                     / (m2.get(iter.key()) + Constants.GetSmallConstant()));
        //				}
      }
    }

    return (divergence);
  }

  // Entropy(m1)
  public static double GetEntropy(TObjectDoubleHashMap m1) {
    double entropy = 0;
    TObjectDoubleIterator iter = m1.iterator();
    while (iter.hasNext()) {
      iter.advance();
      if (iter.value() > 0) {
        entropy += -1 * iter.value() * Math.log(iter.value());
      }
    }

    return (entropy);
  }

}
