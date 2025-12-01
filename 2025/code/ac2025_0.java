package code;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.channels.Pipe.SourceChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ac2025_0 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int solution_num= sc.nextInt();
        String files=sc.nextLine().trim();
        String[] filelist = (files.length()==0)?new String[]{"","t"}:files.split(" ");
        sc.close();
        System.out.println(">>"+String.join(",",filelist));
        runProcess(solution_num, filelist);
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
        String task = "ac2025_0";
        String inputBase = String.format("inputs\\%s%s.txt", task, suffix);
        List<String> data = read(inputBase);
        if (data != null) {
            String result = sol.solve(data);
            System.out.printf("Result for %s: %s%n\n", suffix, result);
        } else {
            System.out.printf("Data missing for %s!\n",suffix);
        }
    }

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
        return "Running template for some reason???";// Default preprocessing (identity function)
    }
}

class Step1 extends Solution {

}

class Step2 extends Step1 {
    
}