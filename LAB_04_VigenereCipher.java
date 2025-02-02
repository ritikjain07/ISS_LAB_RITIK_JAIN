class LAB_04_VigenereCipher {
    
    // Method to generate a repeating key of the same length as the input text
    static String generateKey(String text, String key) {
        StringBuilder extendedKey = new StringBuilder(key);
        int textLength = text.length();
        
        for (int i = 0; extendedKey.length() < textLength; i++) {
            extendedKey.append(key.charAt(i % key.length()));
        }
        
        return extendedKey.toString();
    }

    // Encrypts the given text using the Vigenere Cipher
    static String encrypt(String text, String key) {
        StringBuilder cipherText = new StringBuilder();
        
        for (int i = 0; i < text.length(); i++) {
            int encryptedChar = (text.charAt(i) + key.charAt(i)) % 26 + 'A';
            cipherText.append((char) encryptedChar);
        }
        
        return cipherText.toString();
    }

    // Decrypts the given ciphertext to retrieve the original text
    static String decrypt(String cipherText, String key) {
        StringBuilder originalText = new StringBuilder();
        
        for (int i = 0; i < cipherText.length(); i++) {
            int decryptedChar = (cipherText.charAt(i) - key.charAt(i) + 26) % 26 + 'A';
            originalText.append((char) decryptedChar);
        }
        
        return originalText.toString();
    }

    // Converts lowercase letters to uppercase
    static String toUpperCase(String input) {
        return input.toUpperCase();
    }

    // Driver method
    public static void main(String[] args) {
        String inputText = "Hello there is an attack on monday";
        String keyword = "AYUSH";

        // Convert inputs to uppercase
        inputText = toUpperCase(inputText);
        keyword = toUpperCase(keyword);
        
        // Generate key and perform encryption
        String key = generateKey(inputText, keyword);
        String encryptedText = encrypt(inputText, key);

        System.out.println("Encrypted Text: " + encryptedText);
        System.out.println("Decrypted Text: " + decrypt(encryptedText, key));
    }
}