import java.util.ArrayList;
import java.awt.Robot;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;


class PalindromeGenerator implements KeyListener {
    public static void main(String[] args) {
        // generate7Digits();
        // generate8Digits();
    }
    
    public static void generate7Digits() {
        ArrayList<String> palindromeList = new ArrayList<String>();

        for (int i = 100; i < 1000; i++) {
            String str = String.valueOf(i);
            String reverseStr = reverse(str);
            for (int j = 0; j < 10; j++) {
                palindromeList.add(str + String.valueOf(j) + reverseStr);
            }
        }

        System.out.println(palindromeList);
    }

    public static void generate8Digits() {
        ArrayList<String> palindromeList = new ArrayList<String>();

        for (int i = 1000; i < 10000; i++) {
            String str = String.valueOf(i);
            String reverseStr = reverse(str);
            palindromeList.add(str + reverseStr);
        }

        System.out.println(palindromeList);
    }

    public static String reverse(String str) {
        String newStr = "";
        for (int i = 0; i < str.length(); i++) {
            char ch = str.charAt(i);
            newStr = ch + newStr;
        }
        return newStr;
    }

    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();

        System.out.println(key);
    }

    public void keyReleased(KeyEvent e) {

    }

    public void keyTyped(KeyEvent e) {

    }
}