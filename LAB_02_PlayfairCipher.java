import java.util.Scanner;

public class LAB_02_PlayfairCipher {
    private static char[][] keyMatrix = new char[5][5];

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter the key: ");
        String key = scanner.nextLine();

        System.out.println("Enter the message to encrypt: ");
        String message = scanner.nextLine();

        generateKeyMatrix(key);

        String formattedMessage = formatMessage(message);
        String encryptedMessage = encrypt(formattedMessage);

        System.out.println("Encrypted Message: " + encryptedMessage);

        String decryptedMessage = decrypt(encryptedMessage);
        System.out.println("Decrypted Message: " + decryptedMessage);
    }

    private static void generateKeyMatrix(String key) {
        boolean[] used = new boolean[26];
        key = key.toUpperCase().replaceAll("[^A-Z]", "").replace('J', 'I');
        int index = 0;

        for (char c : key.toCharArray()) {
            if (!used[c - 'A']) {
                keyMatrix[index / 5][index % 5] = c;
                used[c - 'A'] = true;
                index++;
            }
        }

        for (char c = 'A'; c <= 'Z'; c++) {
            if (!used[c - 'A'] && c != 'J') {
                keyMatrix[index / 5][index % 5] = c;
                used[c - 'A'] = true;
                index++;
            }
        }
    }

    private static String formatMessage(String message) {
        message = message.toUpperCase().replaceAll("[^A-Z]", "").replace('J', 'I');
        StringBuilder formatted = new StringBuilder();

        for (int i = 0; i < message.length(); i++) {
            char current = message.charAt(i);
            if (i + 1 < message.length() && current == message.charAt(i + 1)) {
                formatted.append(current).append('X');
            } else {
                formatted.append(current);
            }
        }

        if (formatted.length() % 2 != 0) {
            formatted.append('X');
        }

        return formatted.toString();
    }

    private static String encrypt(String message) {
        StringBuilder encrypted = new StringBuilder();

        for (int i = 0; i < message.length(); i += 2) {
            char a = message.charAt(i);
            char b = message.charAt(i + 1);

            int[] posA = findPosition(a);
            int[] posB = findPosition(b);

            if (posA[0] == posB[0]) { // Same row
                encrypted.append(keyMatrix[posA[0]][(posA[1] + 1) % 5]);
                encrypted.append(keyMatrix[posB[0]][(posB[1] + 1) % 5]);
            } else if (posA[1] == posB[1]) { // Same column
                encrypted.append(keyMatrix[(posA[0] + 1) % 5][posA[1]]);
                encrypted.append(keyMatrix[(posB[0] + 1) % 5][posB[1]]);
            } else { // Rectangle
                encrypted.append(keyMatrix[posA[0]][posB[1]]);
                encrypted.append(keyMatrix[posB[0]][posA[1]]);
            }
        }

        return encrypted.toString();
    }

    private static String decrypt(String message) {
        StringBuilder decrypted = new StringBuilder();

        for (int i = 0; i < message.length(); i += 2) {
            char a = message.charAt(i);
            char b = message.charAt(i + 1);

            int[] posA = findPosition(a);
            int[] posB = findPosition(b);

            if (posA[0] == posB[0]) { // Same row
                decrypted.append(keyMatrix[posA[0]][(posA[1] + 4) % 5]);
                decrypted.append(keyMatrix[posB[0]][(posB[1] + 4) % 5]);
            } else if (posA[1] == posB[1]) { // Same column
                decrypted.append(keyMatrix[(posA[0] + 4) % 5][posA[1]]);
                decrypted.append(keyMatrix[(posB[0] + 4) % 5][posB[1]]);
            } else { // Rectangle
                decrypted.append(keyMatrix[posA[0]][posB[1]]);
                decrypted.append(keyMatrix[posB[0]][posA[1]]);
            }
        }

        return decrypted.toString();
    }

    private static int[] findPosition(char c) {
        for (int row = 0; row < 5; row++) {
            for (int col = 0; col < 5; col++) {
                if (keyMatrix[row][col] == c) {
                    return new int[]{row, col};
                }
            }
        }
        return null; // Should never reach here
    }
}
