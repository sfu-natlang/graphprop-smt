package upenn.junto.graph;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;

import upenn.junto.util.CollectionUtil;
import upenn.junto.type.RyanAlphabet;

import gnu.trove.TObjectDoubleHashMap;
import gnu.trove.TObjectDoubleIterator;

public class LabelGraph {
	private HashMap<String, TObjectDoubleHashMap> labelCov_;
	
	public void LoadLabelGraph(// TObjectDoubleHashMap seedLabels,
							   RyanAlphabet labelAlpha,
							   String inFile) {
		labelCov_ = new HashMap();
		
		// System.out.println("Seed labels: " + CollectionUtil.Map2String(seedLabels) + " " + seedLabels.size());
		// System.out.println("Seed Labels: " + labelAlpha.toString());

		try {
			BufferedReader br = new BufferedReader(new FileReader(inFile));
			String line;
			while ((line = br.readLine()) != null) {
				line.trim();
				// skip comment lines which start with "#"
				if (line.startsWith("#")) {
					continue;
				}
				
				// e.g.: professor teacher 1.0
				String[] parts = line.split("\t");
				assert(parts.length >= 3);
				
				// proceed further only if both labels belong to the
				// seed label set
				// if (!seedLabels.containsKey(parts[0]) ||
				//		!seedLabels.containsKey(parts[1])) {
				// if (!labelAlpha.contains(parts[0]) || 
				//		!labelAlpha.contains(parts[1])) {
				//	continue;
				//}
				
				if (!labelCov_.containsKey(parts[0])) {
					labelCov_.put(parts[0], new TObjectDoubleHashMap());
				}
				if (!labelCov_.containsKey(parts[1])) {
					labelCov_.put(parts[1], new TObjectDoubleHashMap());
				}
				
				// we assume the covariance or similarity constraint to be symmetric
				GetLabelCov(parts[0]).put(parts[1], Double.parseDouble(parts[2]));
				GetLabelCov(parts[1]).put(parts[0], Double.parseDouble(parts[2]));
			}
			br.close();
		} catch (IOException ioe) {
			ioe.printStackTrace();
		}
		
		System.out.println("Total labels for which covariances loaded: " +
				this.labelCov_.size());
	}
	
	public Iterator<Entry<String,TObjectDoubleHashMap>> GetIterator() {
		return (this.labelCov_.entrySet().iterator());
	}
	
	public double GetLabelCovSum(String label) {
		double sum = 0;
		if (this.labelCov_.containsKey(label)) {
			TObjectDoubleIterator iter = GetLabelCov(label).iterator();
			while (iter.hasNext()) {
				iter.advance();
				sum += iter.value();
			}
		}
		return (sum);
	}
	
	public TObjectDoubleHashMap GetLabelCov(String label) {
		// System.out.println("Getting covariance for label: " + label);
		return ((TObjectDoubleHashMap) this.labelCov_.get(label));
	}

	public double GetLabelLabelCov(String label1, String label2) {
		double retVal = -1;
		if (this.labelCov_.containsKey(label1) &&
				GetLabelCov(label1).containsKey(label2)) {
			retVal = GetLabelCov(label1).get(label2);
		}
		return (retVal);
	}
}

