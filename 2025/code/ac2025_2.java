package code;
import java.util.List;
import java.util.ArrayList;

public class ac2025_2 extends ac2025{
    public static void main(String[] args) {
        ac2025_2 main=new ac2025_2();
        main.submain(2);
    }

    public long findLastWrong(long first) {
        if (first<11) return 0;
        String s_first=""+first;
        int half=s_first.length()/2;
        if (s_first.length()%1==1){
            s_first="9".repeat(half);
            return Long.parseLong(s_first.repeat(2));
        }
        long left_half=Long.parseLong(s_first.subSequence(0, half).toString());
        long right_half=Long.parseLong(s_first.subSequence(half,half*2).toString());
        if (left_half>right_half) {left_half--;right_half=left_half;}
        right_half=left_half;
        return right_half;
    }

    public long findAllBelow(long last){
        long b=(""+last).length();
        long res=(long)Math.pow(10, (b-1)/2);
        long halfwrong=findLastWrong(b);
        res+=halfwrong;
        return res;
    }

    public long findRange(long first, long last) {
        long res=0;
        res+=findAllBelow(last);
        res-=findAllBelow(first-1);
        return res;
    }

    public List<Long[]> parseLine(List<String> ls){
        ArrayList<String> pairs=new ArrayList<String>();
        for (String line:ls) {
            String[] temp=line.split(",");
            for (String el:temp) pairs.add(el);
        }
        List<Long[]> res=new ArrayList<Long[]>();
        for (String raw : pairs){
            String[] processed=raw.split("-");
            Long[] nums=new Long[processed.length];
            for (int i=0;i<processed.length;i++) nums[i]=Long.parseLong(processed[i]);
            res.add(nums);
        }
        return res;
    }

    public String step1(List<String> ls) {
        List<Long[]> elements=this.parseLine(ls);
        long res=0;
        for (Long[] el : elements){
            long a=el[0];long b=el[1];
            long tempres=this.findRange(a, b);
            System.out.printf("%s %s|%s",a,b,tempres);
            res+=tempres;
        }
        return "Running step one, result = "+res;// Default preprocessing (identity function)
    }

    public String step2(List<String> ls) {
        return "Running step two";// Default preprocessing (identity function)
    }
}