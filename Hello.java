interface IHello {

}

interface IHello2 {

}

class AException extends Exception {

}

public class Hello implements IHello, IHello2 {

    private static final int a = 0;

    public static final int b = 1;

    public int add(int a, int b) {

        try {
            throw new AException();
        } catch (AException e) {
            b = 2 * b;
        } finally {
            a = 2 * a;
        }

        return a+b;
    }

    private static int sub(int a, int b) {
        return a -b;
    }

}