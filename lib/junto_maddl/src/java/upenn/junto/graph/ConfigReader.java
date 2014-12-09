package upenn.junto.graph;

import upenn.junto.util.MessagePrinter;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Hashtable;
import java.util.StringTokenizer;

public class ConfigReader {
	
  public static Hashtable read_config(String fName) {
    Hashtable retval = new Hashtable(50);
    return (read_config(retval, fName));
  }

  @SuppressWarnings("unchecked")
    public static Hashtable read_config(Hashtable retval, String fName) {
    try {
      // File reading preparation
      FileInputStream fis = new FileInputStream(fName);

      InputStreamReader ir = new InputStreamReader(fis);
      BufferedReader br = new BufferedReader(ir);

      // processing lines into lists
      String line;
      StringTokenizer st;

      line = br.readLine();

      String key = "";
      String value = "";
      while (line != null) {

        System.out.println(line);

        st = new StringTokenizer(line);

        // read this line
        int i = 0;
        boolean noComment = true;
        while (noComment && (st.hasMoreTokens())) {
          String t = st.nextToken();
          if (i == 0) {

            if (t.startsWith("#"))
              noComment = false;

            else
              key = t;
          } else if (i == 2)
            value = t;

          i++;
        }

        // if we find a (( key = value )) line, add it to the HT
        if (i == 3) {
          retval.put(key, value);
        }

        line = br.readLine();
      }
      fis.close();
    } catch (IOException ioe) {
      ioe.printStackTrace();
    }

    return retval;
  }
	
  public static Hashtable read_config(String[] args) {
    Hashtable retVal = read_config(args[0]);
		
    for (int ai = 1; ai < args.length; ++ai) {
      String[] parts = args[ai].split("=");
      if (parts.length == 2 && parts[1].length() > 0) {
        System.out.println(parts[0] + " = " + parts[1]);
        retVal.put(parts[0], parts[1]);
      } else {
        retVal.remove(parts[0]);
        MessagePrinter.Print("Removing argument: " + parts[0] + "\n");
      }
    }

    return (retVal);
  }
	
  public static void AppendOptionValue(Hashtable config,
                                       String key,
                                       String appendValue) {
    if (!config.containsKey(key)) {
      MessagePrinter.PrintAndDie("config doesn't contain key: " + key);
    }
    String currVal = (String) config.get(key);
    config.put(key, currVal + appendValue);
		
    MessagePrinter.Print("Updated " + key + " = " + config.get(key));
  }
}
