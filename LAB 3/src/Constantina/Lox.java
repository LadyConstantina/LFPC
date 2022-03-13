package Constantina;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Lox {
    static boolean hadError = false;

    public static void main(String[] args) throws IOException {
        boolean file = true;
        if (file) {
            runFile("...\\grammar example.txt");
        } else {
            runPrompt();
        }

    }
    private static void runFile(String path) throws IOException {
        byte[] bytes = Files.readAllBytes(Paths.get(path));
        run(new String(bytes, Charset.defaultCharset()));
        if (hadError) System.exit(65);
    }
    private static void runPrompt() throws IOException {
        InputStreamReader input = new InputStreamReader(System.in);
        BufferedReader reader = new BufferedReader(input);

        for (;;) {
            System.out.print("> ");
            String line = reader.readLine();
            if (line == null) break;
            run(line);
            hadError = false;
        }
    }
    private static void run(String source) {
        Scanner scanner = new Scanner(source);
        List<Token> tokens = scanner.scanTokens();

        for (Token token : tokens) {
            if (token.literal != null) {
                System.out.println(token.type + " : " + token.lexeme + ", " + token.literal);
            } else {
                System.out.println(token.type + " : " + token.lexeme);
            }
        }
    }
    static void error(int line, String message) {
        report(line, message);
    }

    private static void report(int line, String message) {
        System.err.println(
                "[line " + line + "] Error : " + message);
        hadError = true;
    }
}

