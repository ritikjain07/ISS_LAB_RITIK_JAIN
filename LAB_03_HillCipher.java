class LAB_03_HillCipher {

    // Generate the key matrix from the key string
    static void getKeyMatrix(String key, int keyMatrix[][]) {
        int k = 0;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                keyMatrix[i][j] = (key.charAt(k)) % 65;
                k++;
            }
        }
    }

    // Encrypt the message
    static void encrypt(int cipherMatrix[][], int keyMatrix[][], int messageVector[][]) {
        int x, i, j;
        for (i = 0; i < 3; i++) {
            for (j = 0; j < 1; j++) {
                cipherMatrix[i][j] = 0;
                for (x = 0; x < 3; x++) {
                    cipherMatrix[i][j] += keyMatrix[i][x] * messageVector[x][j];
                }
                cipherMatrix[i][j] = cipherMatrix[i][j] % 26;
            }
        }
    }

    // Decrypt the ciphertext
    static void decrypt(int decryptedMatrix[][], int inverseKeyMatrix[][], int cipherMatrix[][]) {
        int x, i, j;
        for (i = 0; i < 3; i++) {
            for (j = 0; j < 1; j++) {
                decryptedMatrix[i][j] = 0;
                for (x = 0; x < 3; x++) {
                    decryptedMatrix[i][j] += inverseKeyMatrix[i][x] * cipherMatrix[x][j];
                }
                decryptedMatrix[i][j] = decryptedMatrix[i][j] % 26;
                if (decryptedMatrix[i][j] < 0) {
                    decryptedMatrix[i][j] += 26; // Ensure positive values
                }
            }
        }
    }

    // Find the determinant of a 3x3 matrix
    static int findDeterminant(int[][] matrix) {
        int det = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
                - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
                + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);
        return det % 26;
    }

    // Find the modular inverse of a number modulo 26
    static int modularInverse(int a, int m) {
        a = a % m;
        for (int x = 1; x < m; x++) {
            if ((a * x) % m == 1) {
                return x;
            }
        }
        throw new IllegalArgumentException("Modular inverse does not exist");
    }

    // Find the adjugate matrix of a 3x3 matrix
    static void findAdjugate(int[][] matrix, int[][] adjugate) {
        adjugate[0][0] = (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) % 26;
        adjugate[0][1] = (matrix[0][2] * matrix[2][1] - matrix[0][1] * matrix[2][2]) % 26;
        adjugate[0][2] = (matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1]) % 26;

        adjugate[1][0] = (matrix[1][2] * matrix[2][0] - matrix[1][0] * matrix[2][2]) % 26;
        adjugate[1][1] = (matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]) % 26;
        adjugate[1][2] = (matrix[0][2] * matrix[1][0] - matrix[0][0] * matrix[1][2]) % 26;

        adjugate[2][0] = (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]) % 26;
        adjugate[2][1] = (matrix[0][1] * matrix[2][0] - matrix[0][0] * matrix[2][1]) % 26;
        adjugate[2][2] = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26;

        // Ensure all elements are positive
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (adjugate[i][j] < 0) {
                    adjugate[i][j] += 26;
                }
            }
        }
    }

    // Implement the Hill Cipher
    static void HillCipher(String message, String key) {
        // Key matrix
        int[][] keyMatrix = new int[3][3];
        getKeyMatrix(key, keyMatrix);

        // Check determinant
        int determinant = findDeterminant(keyMatrix);
        if (determinant < 0) determinant += 26;

        // Ensure the determinant is coprime with 26
        if (determinant == 0 || gcd(determinant, 26) != 1) {
            throw new IllegalArgumentException("Invalid key matrix. Determinant must be coprime with 26.");
        }

        // Find modular inverse of the determinant
        int determinantModInverse = modularInverse(determinant, 26);

        // Find inverse key matrix
        int[][] adjugate = new int[3][3];
        findAdjugate(keyMatrix, adjugate);

        int[][] inverseKeyMatrix = new int[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                inverseKeyMatrix[i][j] = (adjugate[i][j] * determinantModInverse) % 26;
                if (inverseKeyMatrix[i][j] < 0) {
                    inverseKeyMatrix[i][j] += 26;
                }
            }
        }

        // Message vector
        int[][] messageVector = new int[3][1];
        for (int i = 0; i < 3; i++) {
            messageVector[i][0] = (message.charAt(i)) % 65;
        }

        // Encryption
        int[][] cipherMatrix = new int[3][1];
        encrypt(cipherMatrix, keyMatrix, messageVector);

        StringBuilder ciphertext = new StringBuilder();
        for (int i = 0; i < 3; i++) {
            ciphertext.append((char) (cipherMatrix[i][0] + 65));
        }
        System.out.println("Ciphertext: " + ciphertext);

        // Decryption
        int[][] decryptedMatrix = new int[3][1];
        decrypt(decryptedMatrix, inverseKeyMatrix, cipherMatrix);

        StringBuilder decryptedText = new StringBuilder();
        for (int i = 0; i < 3; i++) {
            decryptedText.append((char) (decryptedMatrix[i][0] + 65));
        }
        System.out.println("Decrypted Text: " + decryptedText);
    }

    // GCD function
    static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    // Main method
    public static void main(String[] args) {
        String message = "ACT";
        String key = "GYBNQKURP";

        HillCipher(message, key);
    }
}
