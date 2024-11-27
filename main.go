package main

import (
	"fmt"
	"net/http"
	"os"
	"io/ioutil"
	"github.com/tealeg/xlsx"
)

func main() {
	url := "https://docs.google.com/spreadsheets/d/1S3kj0zo_QDERJu7O2QU1J4gMRx-K381m/export?format=xlsx"
	filePath := "download_file.xlsx"

	err := downloadFile(url, filePath)
	if err != nil {
		fmt.Printf("Ошибка загрузки файла: %v\n", err)
		return
	}

	sheetNames, err := getSheetNames(filePath)
	if err != nil {
		fmt.Printf("Ошибка получения имен листов: %v\n", err)
		return
	}

	fmt.Println("Имена листов:", sheetNames)
}

func downloadFile(url, filePath string) error {
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("не удалось загрузить файл: %s", resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	err = ioutil.WriteFile(filePath, body, 0644)
	if err != nil {
		return err
	}

	return nil
}

func getSheetNames(filePath string) ([]string, error) {
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		return nil, fmt.Errorf("файл %s не найден", filePath)
	}

	xlFile, err := xlsx.OpenFile(filePath)
	if err != nil {
		return nil, err
	}

	var sheetNames []string
	for _, sheet := range xlFile.Sheets {
		sheetNames = append(sheetNames, sheet.Name)
	}

	return sheetNames, nil
}
