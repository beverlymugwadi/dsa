import sys
import os


class SparseMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.values = {}  # Using a dictionary to store non-zero values


    @classmethod
    def from_file(cls, matrix_file_path):
        with open(matrix_file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]


        if len(lines) < 2:
            raise ValueError("Input file has wrong format: Missing row/column definitions.")


        rows_match = lines[0].split('=')
        cols_match = lines[1].split('=')


        if len(rows_match) != 2 or len(cols_match) != 2:
            raise ValueError("Input file has wrong format: Missing rows or cols definition.")


        rows = int(rows_match[1])
        cols = int(cols_match[1])


        matrix = cls(rows, cols)


        print(f"Parsing matrix with dimensions: {rows} x {cols}")


        for line in lines[2:]:
            parts = line.strip('()').split(',')
            if len(parts) == 3:
                r, c, v = map(int, parts)
                if 0 <= r < rows and 0 <= c < cols:
                    matrix.set_element(r, c, v)
                else:
                    print(f"Skipping invalid entry: row {r}, col {c}, value {v}")
            else:
                raise ValueError("Input file has wrong format: Invalid entry found.")


        return matrix


    def set_element(self, row, col, value):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError(f"Index out of bounds: row {row}, col {col}")


        if value != 0:
            self.values[f"{row},{col}"] = value
        elif f"{row},{col}" in self.values:
            del self.values[f"{row},{col}"]


    def get_element(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError(f"Index out of bounds: row {row}, col {col}")
        return self.values.get(f"{row},{col}", 0)


    def add(self, matrix):
        result = SparseMatrix(self.rows, self.cols)


        if self.rows == matrix.rows and self.cols == matrix.cols:
            print("Performing addition without swapping.")
            for key in self.values:
                r, c = map(int, key.split(','))
                result.set_element(r, c, self.get_element(r, c) + matrix.get_element(r, c))
            for key in matrix.values:
                if key not in self.values:
                    r, c = map(int, key.split(','))
                    result.set_element(r, c, matrix.get_element(r, c))
        elif self.rows == matrix.cols and self.cols == matrix.rows:
            print("Swapping matrices for addition.")
            for key, value in matrix.values.items():
                r, c = map(int, key.split(','))
                result.set_element(c, r, value)


            for key, value in self.values.items():
                r, c = map(int, key.split(','))
                if c < result.rows and r < result.cols:
                    result.set_element(c, r, value + result.get_element(c, r))
                else:
                    print(f"Skipping out-of-bounds element at ({r}, {c}) during addition")
        else:
            raise ValueError("Matrix dimensions are not compatible for addition.")


        return result


    def subtract(self, matrix):
        result = SparseMatrix(self.rows, self.cols)


        if self.rows == matrix.rows and self.cols == matrix.cols:
            print("Performing subtraction without swapping.")
            for key in self.values:
                r, c = map(int, key.split(','))
                result.set_element(r, c, self.get_element(r, c) - matrix.get_element(r, c))
            for key in matrix.values:
                if key not in self.values:
                    r, c = map(int, key.split(','))
                    result.set_element(r, c, -matrix.get_element(r, c))
        elif self.rows == matrix.cols and self.cols == matrix.rows:
            print("Swapping matrices for subtraction.")
            for key, value in matrix.values.items():
                r, c = map(int, key.split(','))
                result.set_element(c, r, -value)


            for key, value in self.values.items():
                r, c = map(int, key.split(','))
                if c < result.rows and r < result.cols:
                    result.set_element(c, r, value + result.get_element(c, r))
                else:
                    print(f"Skipping out-of-bounds element at ({r}, {c}) during subtraction")
        else:
            raise ValueError("Matrix dimensions must match for subtraction.")


        return result


    def multiply(self, matrix):
        if self.cols != matrix.rows:
            raise ValueError("Invalid matrix dimensions for multiplication.")


        result = SparseMatrix(self.rows, matrix.cols)


        for key, value in self.values.items():
            r1, c1 = map(int, key.split(','))
            for c2 in range(matrix.cols):
                product = value * matrix.get_element(c1, c2)
                if product != 0:
                    result.set_element(r1, c2, result.get_element(r1, c2) + product)


        return result


    def display(self):
        print(f"SparseMatrix ({self.rows} x {self.cols}):")
        for key, value in self.values.items():
            print(f"({key}) = {value}")


def perform_matrix_operation(file1, file2, operation, output_file):
    sample_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'sample_inputs')
    file_path1 = os.path.join(sample_dir, file1)
    file_path2 = os.path.join(sample_dir, file2)


    matrix1 = SparseMatrix.from_file(file_path1)
    matrix2 = SparseMatrix.from_file(file_path2)


    print(f"Matrix 1 Dimensions: {matrix1.rows} x {matrix1.cols}")
    print(f"Matrix 2 Dimensions: {matrix2.rows} x {matrix2.cols}")


    if operation == 'add':
        result = matrix1.add(matrix2)
    elif operation == 'subtract':
        result = matrix1.subtract(matrix2)
    elif operation == 'multiply':
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid operation")
        return


    with open(output_file, 'w') as f:
        f.write(format_output(result))
    print(f"Output written to {output_file}")


def format_output(matrix):
    output = f"rows={matrix.rows}\ncols={matrix.cols}\n"
    for key, value in matrix.values.items():
        output += f"({key}) = {value}\n"
    return output.strip()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python matrixalgo.py <file1> <file2> <operation> <outputFile>")
        print("Operations: add, subtract, multiply")
        sys.exit(1)


    file1, file2, operation, output_file = sys.argv[1:]
    perform_matrix_operation(file1, file2, operation, output_file)

