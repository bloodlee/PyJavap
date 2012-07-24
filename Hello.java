interface IHello {

}

interface IHello2 {

}

public class Hello implements IHello, IHello2 {

    private static final int a = 0;

    public static final int b = 1;

    public int add(int a, int b) {
        return a+b;
    }

    private static int sub(int a, int b) {
        return a -b;
    }

}