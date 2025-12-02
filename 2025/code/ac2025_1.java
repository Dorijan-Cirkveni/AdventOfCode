package code;
import java.util.List;

public class ac2025_1 extends ac2025{
    int SIZE=99+1;
    public static void main(String[] args) {
        ac2025_1 main=new ac2025_1();
        main.submain(1);
    }

    public String step1(List<String> ls) {
        int count=0;
        int status=50;
        for (String entry:ls){
            String raw=entry.substring(1);
            Integer num=Integer.parseInt(raw);
            if (entry.startsWith("R")) num=-num;
            status+=num;status%=this.SIZE;
            if (status==0) count++;
        }
        return ""+count;
    }

    public String step2(List<String> ls) {
        int count=0;
        int status=50;
        for (String entry:ls){
            String raw=entry.substring(1);
            Integer num=Integer.parseInt(raw);
            count+=num/this.SIZE;
            num%=this.SIZE; if (num==0) continue;
            int prefix=entry.startsWith("L")?this.SIZE-1:1;
            while (num>0) {num--;
                status+=prefix;
                status%=this.SIZE;
                if (status==0) count++;
            }
        }
        return ""+count;
    }
}