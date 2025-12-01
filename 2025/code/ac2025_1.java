package code;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.channels.Pipe.SourceChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ac2025_1 {
    public static void main(String[] args) {
        String[] filelist = new String[]{"t"};
        runProcess(2, filelist);
    }

    private static void runProcess(int process, String[] inputFiles) {
        if (inputFiles == null) {
            inputFiles = new String[]{""};
        }
        for (String suffix : inputFiles) {
            runProcessWithInputFrom(process, suffix);
        }
    }

    private static void runProcessWithInputFrom(int process, String suffix) {
        Solution sol=new Step2();
        if (process==1) sol=new Step1();
        String task = "ac2025_1";
        String inputBase = String.format("inputs\\%s%s.txt", task, suffix);
        List<String> data = read(inputBase);
        if (data != null) {
            System.out.println(data.size());
            String result = sol.solve(data);
            System.out.println("Result for "+suffix+":"+"\n"+result);
        } else {
            System.out.printf("Data missing for %s!\n",suffix);
        }
    } //

    private static List<String> read(String filepath) {
        List<String> lines = null;
        try (BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            lines = new ArrayList<>();
            String line;
            while ((line = reader.readLine()) != null) {
                lines.add(line);
            }
        } catch (IOException err) {
            System.err.println(err.getMessage());
        }
        return lines;
    }

}

class Solution {

    public String solve(List<String> ls) {
        return "Error";// Default preprocessing (identity function)
    }
}

class Step1 extends Solution {

    public String solve(List<String> ls) {
        int count=0;
        int status=50;
        for (String entry:ls){
            String raw=entry.substring(1);
            Integer num=Integer.parseInt(raw);
            if (entry.startsWith("R")) num=-num;
            status+=num;status%=100;
            if (status==0) count++;
        }
        return ""+count;
    }

}

class Step2 extends Step1 {
    
}