import pandas as pd
import os
import re
import numpy as np
from pathlib import Path

# Define input and output directories
INPUT_DIR = "Jumia Data/raw"
OUTPUT_DIR = "Jumia Data/processed"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_and_inspect_data(file_path):
    """
    Load a CSV file and perform basic inspection
    """
    print(f"\nInspecting {os.path.basename(file_path)}...")
    
    # Load data
    df = pd.read_csv(file_path)
    
    # Basic inspection
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Data types:\n{df.dtypes}")
    
    return df

def standardize_column_names(df):
    """
    Standardize column names to lowercase snake_case
    """
    # Convert to lowercase and replace spaces with underscores
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    return df

def clean_price_data(df):
    """
    Clean and standardize price columns
    """
    # Rename product_price to price for consistency
    if 'product_price' in df.columns:
        df = df.rename(columns={'product_price': 'price'})
    
    # Handle price columns - extract numeric values and convert to float
    price_columns = [col for col in df.columns if 'price' in col.lower()]
    
    for col in price_columns:
        if col in df.columns:
            # Check if the column is already numeric
            if not pd.api.types.is_numeric_dtype(df[col]):
                # Extract numbers from price strings
                df[col] = df[col].astype(str).str.extract(r'(\d+[\d\.,]*)', expand=False)
                
                # Replace commas and convert to float
                df[col] = df[col].str.replace(',', '').astype(float)
    
    # If there are multiple price columns, ensure they are all in NGN
    # For this demo, we'll assume all prices are already in NGN
    
    return df

def extract_attributes(df, category_name):
    """
    Extract key attributes from product information
    """
    # Add category column if not present
    if 'category' not in df.columns:
        df['category'] = category_name
    
    # Clean product names
    if 'product_name' in df.columns:
        # Rename to 'name' for consistency
        df = df.rename(columns={'product_name': 'name'})
        
        # Remove extra spaces
        df['name'] = df['name'].str.strip()
        # Fix capitalization (title case)
        df['name'] = df['name'].str.title()
    
    # Extract size information if it's in the product name or use the sizes column
    if 'name' in df.columns and 'extracted_size' not in df.columns:
        # Common size patterns
        size_pattern = r'\b(XS|S|M|L|XL|XXL|XXXL|[0-9]+)\b'
        df['extracted_size'] = df['name'].str.extract(size_pattern, expand=False)
        
        # If there's a sizes column, use that when extracted_size is null
        if 'sizes' in df.columns:
            mask = df['extracted_size'].isnull()
            df.loc[mask, 'extracted_size'] = df.loc[mask, 'sizes']
    
    # Extract brand information
    if 'name' in df.columns and 'brand' not in df.columns:
        # Try to extract brand name (this is a simple example, might need refinement)
        df['brand'] = df['name'].str.split(' ').str[0]
    
    return df

def handle_missing_and_duplicates(df):
    """
    Handle missing values and remove duplicates
    """
    # Count missing values before cleaning
    missing_before = df.isnull().sum().sum()
    
    # Fill missing values for numeric columns with 0
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # Fill missing values for string columns with 'Unknown'
    string_cols = df.select_dtypes(include=['object']).columns
    df[string_cols] = df[string_cols].fillna('Unknown')
    
    # Remove duplicates
    duplicates_count = df.duplicated().sum()
    df = df.drop_duplicates()
    
    # Report results
    missing_after = df.isnull().sum().sum()
    print(f"Handled {missing_before} missing values, {missing_after} remaining")
    print(f"Removed {duplicates_count} duplicate rows")
    
    return df

def feature_engineering(df):
    """
    Create new features from existing data
    """
    # Calculate discount percentage if price_info contains both old and new prices
    if 'price_info' in df.columns and 'price' in df.columns:
        try:
            # Try to extract old price from price_info
            df['old_price'] = df['price_info'].str.extract(r'old price ₦([\d,]+)', expand=False)
            df['old_price'] = pd.to_numeric(df['old_price'].str.replace(',', ''), errors='coerce')
            
            # Calculate discount percentage where old_price is valid
            mask = (df['old_price'].notnull()) & (df['old_price'] > 0)
            if mask.any():
                df.loc[mask, 'discount_percentage'] = (
                    (df.loc[mask, 'old_price'] - df.loc[mask, 'price']) / df.loc[mask, 'old_price'] * 100
                )
                df['discount_percentage'] = df['discount_percentage'].round(2)
        except Exception as e:
            print(f"Warning: Could not calculate discount percentages - {e}")
    
    return df

def process_file(file_path):
    """
    Process a single Jumia products file
    """
    # Extract category name from file name
    category_name = os.path.basename(file_path).split('_')[-1].split('.')[0]
    print(f"\nProcessing {category_name} products...")
    
    # Load and inspect data
    df = load_and_inspect_data(file_path)
    
    # Apply preprocessing steps
    df = standardize_column_names(df)
    df = clean_price_data(df)
    df = extract_attributes(df, category_name)
    df = handle_missing_and_duplicates(df)
    df = feature_engineering(df)
    
    # Save processed data
    output_path = os.path.join(OUTPUT_DIR, f"processed_{category_name}.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved processed data to {output_path}")
    
    return df

def combine_datasets(dataframes):
    """
    Combine all processed datasets into a single file
    """
    # Combine all dataframes
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Save combined dataset
    output_path = os.path.join(OUTPUT_DIR, "combined_jumia_products.csv")
    combined_df.to_csv(output_path, index=False)
    print(f"\nSaved combined dataset with {len(combined_df)} records to {output_path}")
    
    return combined_df

def create_summary_statistics(df):
    """
    Generate summary statistics by category
    """
    print("\nGenerating summary statistics...")
    summary_path = os.path.join(OUTPUT_DIR, "summary_statistics.csv")
    
    # Create a dictionary for aggregation functions based on available columns
    agg_dict = {}
    
    # Check which columns exist before adding to aggregation
    if 'price' in df.columns:
        agg_dict['price'] = ['count', 'mean', 'min', 'max']
    
    if 'discount_percentage' in df.columns:
        agg_dict['discount_percentage'] = ['mean', 'min', 'max']
    
    # Get counts of products per category if no price column
    if not agg_dict:
        category_counts = df['category'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        category_counts.to_csv(summary_path, index=False)
    else:
        # Group by category and aggregate
        summary = df.groupby('category').agg(agg_dict)
        summary.to_csv(summary_path)
    
    print(f"Saved summary statistics to {summary_path}")

def main():
    # Get list of CSV files
    file_paths = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.endswith('.csv')]
    
    # Process each file
    processed_dfs = []
    for file_path in file_paths:
        df = process_file(file_path)
        processed_dfs.append(df)
    
    # Combine all datasets
    combined_df = combine_datasets(processed_dfs)
    
    # Generate summary statistics
    create_summary_statistics(combined_df)
    
    print("\nPreprocessing complete!")

if __name__ == "__main__":
    main() 