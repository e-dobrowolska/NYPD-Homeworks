import csv_stats as css

def run_analysis(input_path, output_path):
    df = css.load_csv(input_path)
    results = css.calculate_stats(df)
    css.save_csv(results, output_path)
    return

#run_analysis('iris.csv', 'results.csv')
#OK