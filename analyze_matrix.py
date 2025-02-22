import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the confusion matrix image
matrix_path = "confusion_matrix_normalized.png"
img = cv2.imread(matrix_path)

if img is not None:
    # Display basic information
    print("Analyzing confusion matrix...")
    print(f"Image dimensions: {img.shape}")
    
    # Convert BGR to RGB for proper display
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Display the confusion matrix with proper labels
    plt.figure(figsize=(10, 8))
    plt.imshow(img_rgb)
    plt.title("Normalized Confusion Matrix Analysis")
    plt.axis('off')
    plt.savefig('analyzed_matrix.png')
    
    print("\nAnalysis complete. Check 'analyzed_matrix.png' for the visualization.")
    print("\nNote: The confusion matrix shows the model's performance across different classes.")
    print("- Diagonal elements represent correct predictions")
    print("- Off-diagonal elements represent misclassifications")
else:
    print("Error: Could not read the confusion matrix image.")
