# DataCrafter

DataCrafter is a project that involves downloading and processing Excel files. The project has been rewritten in Go to improve performance and maintainability.

## Running the Go Version

To run the Go version of the project, follow these steps:

1. Install Go from the official website: https://golang.org/dl/
2. Clone the repository:
   ```sh
   git clone https://github.com/Lemetist/DataCrafter.git
   cd DataCrafter
   ```
3. Initialize the Go module:
   ```sh
   go mod init github.com/Lemetist/DataCrafter
   go mod tidy
   ```
4. Run the main Go file:
   ```sh
   go run main.go
   ```

## Purpose and Functionality of Go Files

### `main.go`

- Handles HTTP requests and responses.
- Downloads the Excel file from the given URL.
- Parses the Excel file and extracts sheet names.

### `filter_excel.go`

- Filters Excel data based on specific criteria.
- Splits lists and formats data.
- Filters subjects and formats the output.

### `ui.go`

- Creates and manages the user interface.
- Handles button clicks and displays messages.
- Loads and displays filtered data.

## Examples

### Example 1: Running the Project

```sh
go run main.go
```

This command will download the Excel file, parse it, and print the sheet names.

### Example 2: Filtering Excel Data

To filter Excel data based on specific criteria, you can use the functions provided in `filter_excel.go`. For example:

```go
package main

import (
    "fmt"
    "github.com/tealeg/xlsx"
)

func main() {
    filePath := "download_file.xlsx"
    sheetName := "Sheet1"
    result, err := filterExcel(filePath, sheetName)
    if err != nil {
        fmt.Printf("Error filtering Excel data: %v\n", err)
        return
    }
    fmt.Println("Filtered Data:", result)
}
```

### Example 3: Creating and Managing the User Interface

To create and manage the user interface, you can use the functions provided in `ui.go`. For example:

```go
package main

import (
    "github.com/andlabs/ui"
)

func main() {
    err := ui.Main(func() {
        app := &App{}
        app.initUI()
        app.loadDays()
        app.window.Show()
    })
    if err != nil {
        panic(err)
    }
}
```

This will create a simple user interface with a text output and buttons to interact with the data.
