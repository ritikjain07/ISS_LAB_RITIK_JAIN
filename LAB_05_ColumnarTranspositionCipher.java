import java.util.*;

public class LAB_05_ColumnarTranspositionCipher {

    // Method to encrypt the plaintext using Columnar Transposition Cipher
    public static String encrypt(String plaintext, String key) {
        // Remove spaces from the plaintext and convert to uppercase
        plaintext = plaintext.replaceAll("\\s", "").toUpperCase();
        key = key.toUpperCase();

        // Determine the number of columns based on the key length
        int columns = key.length();
        int rows = (int) Math.ceil((double) plaintext.length() / columns);

        // Create a grid to hold the plaintext
        char[][] grid = new char[rows][columns];

        // Fill the grid row-wise with the plaintext
        int index = 0;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                if (index < plaintext.length()) {
                    grid[i][j] = plaintext.charAt(index++);
                } else {
                    grid[i][j] = 'X'; // Padding with 'X' if necessary
                }
            }
        }

        // Determine the column order based on the key
        int[] columnOrder = getColumnOrder(key);

        // Build the ciphertext by reading columns in the order of the key
        StringBuilder ciphertext = new StringBuilder();
        for (int col : columnOrder) {
            for (int i = 0; i < rows; i++) {
                ciphertext.append(grid[i][col]);
            }
        }

        return ciphertext.toString();
    }

    // Method to decrypt the ciphertext using Columnar Transposition Cipher
    public static String decrypt(String ciphertext, String key) {
        key = key.toUpperCase();

        // Determine the number of columns based on the key length
        int columns = key.length();
        int rows = (int) Math.ceil((double) ciphertext.length() / columns);

        // Create a grid to hold the ciphertext
        char[][] grid = new char[rows][columns];

        // Determine the column order based on the key
        int[] columnOrder = getColumnOrder(key);

        // Fill the grid column-wise with the ciphertext
        int index = 0;
        for (int col : columnOrder) {
            for (int i = 0; i < rows; i++) {
                if (index < ciphertext.length()) {
                    grid[i][col] = ciphertext.charAt(index++);
                }
            }
        }

        // Build the plaintext by reading the grid row-wise
        StringBuilder plaintext = new StringBuilder();
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                plaintext.append(grid[i][j]);
            }
        }

        // Remove any padding characters (e.g., 'X')
        return plaintext.toString().replaceAll("X", "");
    }

    // Helper method to determine the column order based on the key
    private static int[] getColumnOrder(String key) {
        // Create a list of column indices sorted by the key's alphabetical order
        List<Integer> columnIndices = new ArrayList<>();
        for (int i = 0; i < key.length(); i++) {
            columnIndices.add(i);
        }

        // Sort the column indices based on the key's characters
        columnIndices.sort(Comparator.comparingInt(i -> key.charAt(i)));

        // Convert the list to an array
        int[] columnOrder = new int[key.length()];
        for (int i = 0; i < columnIndices.size(); i++) {
            columnOrder[i] = columnIndices.get(i);
        }

        return columnOrder;
    }

    // Main method to test the Columnar Transposition Cipher
    public static void main(String[] args) {
        String plaintext = "HELLOWORLD";
        String key = "KEY";

        // Encrypt the plaintext
        String ciphertext = encrypt(plaintext, key);
        System.out.println("Encrypted: " + ciphertext);

        // Decrypt the ciphertext
        String decryptedText = decrypt(ciphertext, key);
        System.out.println("Decrypted: " + decryptedText);
    }
}