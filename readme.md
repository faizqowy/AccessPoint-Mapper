# AccessPoint-Mapper

AccessPoint-Mapper is a tool designed to help you map and manage wireless access points efficiently.

## Usage

First, analyze your access point data by running:

```bash
python analyzer.py
```

After analysis, you can convert the result into a CSV file with:

```bash
python log_to_format.py csv -o wifi_log.csv
```

You can replace `wifi_log.csv` with any filename you prefer for the output.

## Features

- Import access point data from CSV or JSON.
- Export mapped data in multiple formats.

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Submit a pull request.

## License

This project is licensed under the MIT License.
