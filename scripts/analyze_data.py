import csv
import math
import random
import json

def read_data(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        missing_count = 0
        row_count = 0
        for row in reader:
            row_count += 1
            if not row or any(val == '' for val in row):
                missing_count += 1
                continue
            try:
                vals = [float(x) for x in row]
                data.append(vals)
            except ValueError:
                missing_count += 1
    return header, data, row_count, missing_count

def calc_stats(values):
    n = len(values)
    if n == 0:
        return {}
    s_sorted = sorted(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0.0
    std_dev = math.sqrt(variance)
    min_val = s_sorted[0]
    max_val = s_sorted[-1]
    
    def percentile(s, p):
        k = (len(s) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return s[int(k)]
        d0 = s[int(f)] * (c - k)
        d1 = s[int(c)] * (k - f)
        return d0 + d1

    q25 = percentile(s_sorted, 25)
    median = percentile(s_sorted, 50)
    q75 = percentile(s_sorted, 75)
    
    return {
        "count": n,
        "mean": mean,
        "std": std_dev,
        "min": min_val,
        "25%": q25,
        "50%": median,
        "75%": q75,
        "max": max_val
    }

def pearson_corr(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    den_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)))
    den_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)

# Matrix operations for OLS
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def matmul(A, B):
    result = [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in transpose(B)] for row_a in A]
    return result

def invert_matrix(matrix):
    # Gaussian elimination with partial pivoting for square matrix
    n = len(matrix)
    identity = [[float(i == j) for j in range(n)] for i in range(n)]
    m = [row[:] + identity[row_idx] for row_idx, row in enumerate(matrix)]
    
    for i in range(n):
        # Pivot
        max_el = abs(m[i][i])
        max_row = i
        for k in range(i + 1, n):
            if abs(m[k][i]) > max_el:
                max_el = abs(m[k][i])
                max_row = k
        m[i], m[max_row] = m[max_row], m[i]
        
        pivot = m[i][i]
        if abs(pivot) < 1e-12:
            raise ValueError("Matrix is singular or nearly singular.")
        
        for j in range(2 * n):
            m[i][j] /= pivot
            
        for k in range(n):
            if k != i:
                factor = m[k][i]
                for j in range(2 * n):
                    m[k][j] -= factor * m[i][j]
                    
    inverse = [row[n:] for row in m]
    return inverse

def linear_regression(X, y):
    # X is N x K (including column of 1s), y is N x 1
    XT = transpose(X)
    XTX = matmul(XT, X)
    XTX_inv = invert_matrix(XTX)
    XTy = matmul(XT, [[val] for val in y])
    beta_matrix = matmul(XTX_inv, XTy)
    return [row[0] for row in beta_matrix]

def evaluate_model(X, y, beta):
    n = len(y)
    predictions = []
    for row in X:
        pred = sum(r * b for r, b in zip(row, beta))
        predictions.append(pred)
    
    residuals = [y[i] - predictions[i] for i in range(n)]
    mse = sum(r ** 2 for r in residuals) / n
    rmse = math.sqrt(mse)
    mae = sum(abs(r) for r in residuals) / n
    
    mean_y = sum(y) / n
    ss_tot = sum((val - mean_y) ** 2 for val in y)
    ss_res = sum(r ** 2 for r in residuals)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
    
    return {
        "R2": r2,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "predictions": predictions,
        "residuals": residuals
    }

def main():
    header, data, total_rows, missing_count = read_data("Folds5x2_pp.csv")
    print(f"Header: {header}")
    print(f"Total rows read: {len(data)}, Skipped/Missing: {missing_count}")
    
    # Column statistics
    cols = list(zip(*data))
    stats = {}
    for idx, name in enumerate(header):
        stats[name] = calc_stats(cols[idx])
        
    # Correlation matrix
    corr_matrix = {}
    for i, name_i in enumerate(header):
        corr_matrix[name_i] = {}
        for j, name_j in enumerate(header):
            corr_matrix[name_i][name_j] = pearson_corr(cols[i], cols[j])
            
    # OLS Regression on full dataset
    # Features: AT, V, AP, RH -> PE
    # X matrix: [1, AT, V, AP, RH]
    X_full = [[1.0, row[0], row[1], row[2], row[3]] for row in data]
    y_full = [row[4] for row in data]
    
    beta = linear_regression(X_full, y_full)
    full_eval = evaluate_model(X_full, y_full, beta)
    
    # 80/20 train/test split
    random.seed(42)
    indexed_data = list(enumerate(data))
    random.shuffle(indexed_data)
    train_size = int(0.8 * len(data))
    train_data = [row for _, row in indexed_data[:train_size]]
    test_data = [row for _, row in indexed_data[train_size:]]
    
    X_train = [[1.0, row[0], row[1], row[2], row[3]] for row in train_data]
    y_train = [row[4] for row in train_data]
    X_test = [[1.0, row[0], row[1], row[2], row[3]] for row in test_data]
    y_test = [row[4] for row in test_data]
    
    beta_train = linear_regression(X_train, y_train)
    train_eval = evaluate_model(X_train, y_train, beta_train)
    test_eval = evaluate_model(X_test, y_test, beta_train) # evaluate test set using train coefficients
    
    report = {
        "dataset_info": {
            "total_rows_file": total_rows,
            "valid_rows_used": len(data),
            "missing_rows": missing_count,
            "columns": header
        },
        "descriptive_statistics": stats,
        "correlation_matrix": corr_matrix,
        "ols_coefficients_full": {
            "beta_0 (Intercept)": beta[0],
            "beta_1 (AT)": beta[1],
            "beta_2 (V)": beta[2],
            "beta_3 (AP)": beta[3],
            "beta_4 (RH)": beta[4]
        },
        "model_performance_full": {
            "R2": full_eval["R2"],
            "MAE": full_eval["MAE"],
            "MSE": full_eval["MSE"],
            "RMSE": full_eval["RMSE"]
        },
        "train_performance": {
            "R2": train_eval["R2"],
            "MAE": train_eval["MAE"],
            "MSE": train_eval["MSE"],
            "RMSE": train_eval["RMSE"]
        },
        "test_performance": {
            "R2": test_eval["R2"],
            "MAE": test_eval["MAE"],
            "MSE": test_eval["MSE"],
            "RMSE": test_eval["RMSE"]
        },
        "ols_coefficients_train": {
            "beta_0 (Intercept)": beta_train[0],
            "beta_1 (AT)": beta_train[1],
            "beta_2 (V)": beta_train[2],
            "beta_3 (AP)": beta_train[3],
            "beta_4 (RH)": beta_train[4]
        }
    }
    
    with open("analysis_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
        
    print("Analysis complete. Saved to analysis_report.json")
    print(json.dumps(report, indent=4))

if __name__ == "__main__":
    main()
