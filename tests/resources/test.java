import java.io.*;
import java.util.*;

public class CumulativeSum {
    public static void main(String[] args) {
        // Path to the input and output files
        String inputFile = "input.txt";
        String outputFile = "result.txt";

        try {
            // Create a Scanner to read from the file
            Scanner scanner = new Scanner(new File(inputFile));
            
            // Read the first number, which is n (the number of subsequent numbers)
            int n = scanner.nextInt();
            
            // Create an array to store the n numbers
            int[] numbers = new int[n];
            
            // Read the next n numbers into the array
            for (int i = 0; i < n; i++) {
                numbers[i] = scanner.nextInt();
            }
            
            // Create a BufferedWriter to write to the output file
            BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));

            // Calculate and write the cumulative sums
            int cumulativeSum = 0;
            for (int i = 0; i < n; i++) {
                cumulativeSum += numbers[i];
                writer.write(Integer.toString(cumulativeSum));  // Write the cumulative sum as a string
                writer.newLine();  // Write a new line after each sum
            }
            
            // Close the scanner and the writer
            scanner.close();
            writer.close();
            
            System.out.println("The cumulative sums have been written to " + outputFile);
        } catch (FileNotFoundException e) {
            System.out.println("Error: The file " + inputFile + " was not found.");
        } catch (IOException e) {
            System.out.println("Error: An IO error occurred: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
