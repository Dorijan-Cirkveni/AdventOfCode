package code;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
// import java.nio.channels.Pipe.SourceChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ac2025 {
    public static void main(String[] args) {
        ac2025 main=new ac2025();
        main.submain(0);
    }

    public String step1(List<String> ls) {
        return "Running step 1";// Default preprocessing (identity function)
    }

    public String step2(List<String> ls) {
        return "Running step 2";// Default preprocessing (identity function)
    }

    public void submain(int tasknum){
        Scanner sc = new Scanner(System.in);
        int solution_num= sc.nextInt();
        String files=sc.nextLine().trim();
        String[] filelist = (files.length()==0)?new String[]{"","t"}:files.split(" ");
        sc.close();
        System.out.println(">>"+String.join(",",filelist));
        this.runProcess(tasknum, solution_num, filelist);
    }

    private void runProcess(int tasknum, int process, String[] inputFiles) {
        if (inputFiles == null) {
            inputFiles = new String[]{"","t"};
        }
        for (String suffix : inputFiles) {
            this.runProcessWithInputFrom(tasknum, process, suffix);
        }
    }

    private void runProcessWithInputFrom(int tasknum, int process, String suffix) {
        String task = "2025_"+tasknum;
        String address = "inputs\\"+task+suffix+".txt";
        System.out.println(address);
        List<String> data = this.read(address);
        if (data == null) {System.out.printf("Data missing for %s!\n",suffix); return;}
        String result = "No result.";
        switch (process) {
            case 1:
                result = this.step1(data);
                break;
        
            case 2:
                result = this.step2(data);
                break;

            default:
                break;
        }
        System.out.printf("Result for %s: %s%n\n", suffix, result);
    }

    private List<String> read(String filepath) {
        List<String> lines = null;
        try {
            FileReader fread=new FileReader(filepath);
            BufferedReader reader = new BufferedReader(fread);
            System.out.println("Reading...");
            lines = new ArrayList<>();
            String line;
            while ((line = reader.readLine()) != null) {
                lines.add(line);
            }
            reader.close();
            fread.close();
        } catch (IOException err) {
            System.err.println("IO Exception:"+err.getMessage());
        }
        return lines;
    }

}
