package code;
import java.util.List;
import java.util.ArrayList;
import java.util.InputMismatchException;

public class ac2025_2 extends ac2025{
    public static void main(String[] args) {
        ac2025_2 main=new ac2025_2();
        main.submain(2);
    }

    public static long gaussSum(long n) {return (n*(n+1))/2;}

    public static long gaussDiff(long a, long b) {return gaussSum(b)-gaussSum(a);}

    public long findLastWrong(long first) {
        if (first<11) return 0;
        String s_first=""+first;
        int half=s_first.length()/2;
        if (s_first.length()%2==1){
            s_first="9".repeat(half);
            return Long.parseLong(s_first);
        }
        long left_half=Long.parseLong(s_first.subSequence(0, half).toString());
        long right_half=Long.parseLong(s_first.subSequence(half,half*2).toString());
        if (left_half>right_half) {left_half--;right_half=left_half;}
        right_half=left_half;
        return right_half;
    }

    public long sumAllBelow(long last){
        long halfwrong=findLastWrong(last);
        long res=0;
        long cur=1;
        // System.out.println(""+cur+"-"+halfwrong);
        while (cur<=halfwrong) {
            long nex=Math.min(halfwrong+1, cur*10);
            long cur_res=gaussDiff(cur-1, nex-1);
            if(cur>nex) throw new InputMismatchException();
            cur_res*=cur*10+1;
            // System.out.println("> "+cur+"\t"+nex+"\t"+cur_res);
            res+=cur_res;
            cur=nex;
        }
        return res;
    }

    public long sumRange(long first, long last) {
        long res=0;
        res+=sumAllBelow(last);
        res-=sumAllBelow(first-1);
        return res;
    }

    public static Long expand(Long cur, int repeats){
        return Long.parseLong(cur.toString().repeat(repeats));
    }
    public static boolean isPair(Long cur){
        String check=cur.toString();
        int len=check.length();
        if (len%2==1) return false;
        len/=2;
        return check.substring(0,len).equals(check.substring(len));
    }
    public long sumRange(long first, long last, int repeats){
        Long cur=0L;
        Long cur_ref=0L;
        while (cur_ref<first) {
            cur++; cur_ref=expand(cur, repeats);
        }
        Long res=0L;
        while (cur_ref<=last) {
            if (!isPair(cur)) res+=cur_ref;
            cur++;
            cur_ref=expand(cur, repeats);
        }
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
        long maxval=0;
        for (Long[] el : elements){
            long a=el[0];long b=el[1];
            long tempres=this.sumRange(a, b);
            maxval=Math.max(maxval, b);
            // System.out.printf("%s\t\t%s|%s\n",a,b,tempres);
            res+=tempres;
        }
        return "Running step one, max="+maxval+", result = "+res;// Default preprocessing (identity function)
    }

    public String step2(List<String> ls) {
        List<Long[]> elements=this.parseLine(ls);
        long res=0;
        long maxval=0;
        for (Long[] el : elements){
            long a=el[0];long b=el[1];
            long tempres=this.sumRange(a, b);
            tempres+=this.sumRange(a, b, 3);
            tempres+=this.sumRange(a, b, 5);
            tempres+=this.sumRange(a, b, 7);
            tempres+=this.sumRange(a, b, 11);
            maxval=Math.max(maxval, b);
            // System.out.printf("%s\t\t%s|%s\n",a,b,tempres);
            res+=tempres;
        }
        return "Running step one, max="+maxval+", result = "+res;// Default preprocessing (identity function)
    }
}