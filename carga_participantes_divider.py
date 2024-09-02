import pandas as pd
import os
import csv

def split_csv(file_path, lines_per_file=1000):
    error_lines = []
    output_dir = os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0])
    os.makedirs(output_dir, exist_ok=True)
    
    error_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}_erros_encontrados.csv")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Lendo o header
            line_number = 1  # Inicia após o header

            # Criando o arquivo de erros com o header
            with open(error_file_path, 'w', encoding='utf-8', newline='') as error_file:
                error_writer = csv.writer(error_file)
                error_writer.writerow(header)

                data_rows = []
                for line in reader:
                    line_number += 1
                    try:
                        # Tentando processar a linha como uma lista de campos
                        if len(line) != len(header):
                            raise ValueError(f"Erro de formatação na linha {line_number}: número incorreto de campos.")
                        data_rows.append(line)
                    except Exception as e:
                        # Se falhar, salva a linha no arquivo de erros
                        error_lines.append(line)
                        error_writer.writerow(line)
            
            # Converte as linhas bem sucedidas em um DataFrame
            if data_rows:
                df = pd.DataFrame(data_rows, columns=header)
                total_lines = len(df)
                num_parts = (total_lines + lines_per_file - 1) // lines_per_file  # Calcula o número de partes

                for i in range(num_parts):
                    start_row = i * lines_per_file
                    end_row = min(start_row + lines_per_file, total_lines)
                    part_df = df.iloc[start_row:end_row]
                    part_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}_parte-{i+1}.csv")
                    part_df.to_csv(part_file_path, index=False)

        if error_lines:
            print(f"{len(error_lines)} linha(s) mal formatada(s) foram encontradas e salvas em {error_file_path}.")
        else:
            os.remove(error_file_path)  # Remove o arquivo de erros se nenhum erro foi encontrado
            print("O arquivo foi dividido com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    file_path = input("Digite o caminho do arquivo CSV: ")
    lines_per_file = input("Número de linhas por arquivo (padrão 1000): ")
    lines_per_file = int(lines_per_file) if lines_per_file.isdigit() else 1000
    split_csv(file_path, lines_per_file)

