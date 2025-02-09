// Java implementation of the Rail Fence Cipher for encryption and decryption
import java.util.Arrays;

public class LAB_05_railFenceCipher {

    // Method to encrypt the plaintext using Rail Fence Cipher
    public static String encrypt(String plaintext, int rails) {
        char[][] railMatrix = new char[rails][plaintext.length()];

        // Initialize the rail matrix with placeholder characters
        for (char[] row : railMatrix) {
            Arrays.fill(row, '.');
        }

        int currentRow = 0;
        boolean movingDown = true;

        for (int i = 0; i < plaintext.length(); i++) {
            railMatrix[currentRow][i] = plaintext.charAt(i);

            if (currentRow == 0) {
                movingDown = true;
            } else if (currentRow == rails - 1) {
                movingDown = false;
            }

            currentRow += movingDown ? 1 : -1;
        }

        // Build the encrypted message from the rail matrix
        StringBuilder encryptedText = new StringBuilder();
        for (char[] row : railMatrix) {
            for (char ch : row) {
                if (ch != '.') {
                    encryptedText.append(ch);
                }
            }
        }

        return encryptedText.toString();
    }

    // Method to decrypt the ciphertext using Rail Fence Cipher
    public static String decrypt(String ciphertext, int rails) {
        char[][] railMatrix = new char[rails][ciphertext.length()];

        // Initialize the rail matrix with placeholder characters
        for (char[] row : railMatrix) {
            Arrays.fill(row, '.');
        }

        int currentRow = 0;
        boolean movingDown = true;

        // Mark the positions in the rail matrix where characters should be placed
        for (int i = 0; i < ciphertext.length(); i++) {
            railMatrix[currentRow][i] = '*';

            if (currentRow == 0) {
                movingDown = true;
            } else if (currentRow == rails - 1) {
                movingDown = false;
            }

            currentRow += movingDown ? 1 : -1;
        }

        // Fill the rail matrix with the ciphertext characters
        int index = 0;
        for (int i = 0; i < rails; i++) {
            for (int j = 0; j < ciphertext.length(); j++) {
                if (railMatrix[i][j] == '*' && index < ciphertext.length()) {
                    railMatrix[i][j] = ciphertext.charAt(index++);
                }
            }
        }

        // Reconstruct the original message
        StringBuilder decryptedText = new StringBuilder();
        currentRow = 0;
        movingDown = true;

        for (int i = 0; i < ciphertext.length(); i++) {
            decryptedText.append(railMatrix[currentRow][i]);

            if (currentRow == 0) {
                movingDown = true;
            } else if (currentRow == rails - 1) {
                movingDown = false;
            }

            currentRow += movingDown ? 1 : -1;
        }

        return decryptedText.toString();
    }

    // Main method to test the Rail Fence Cipher
    public static void main(String[] args) {
        // Test encryption
        System.out.println("Encrypted Messages:");
        System.out.println(encrypt("attack at once", 2)); 
        System.out.println(encrypt("on the sea shore ", 3)); 
        System.out.println(encrypt("defend the east wall", 3));

        // Test decryption
        System.out.println("\nDecrypted Messages:");
        System.out.println(decrypt("atc toctaka ne", 2));
        System.out.println(decrypt("oheh ntesasoe   r", 3));
        System.out.println(decrypt("dnhaweedtees alf tl", 3));
    }
}