package main

import (
	"fmt"
	"os"
	"github.com/tealeg/xlsx"
	"math"
)

func wbName() ([]string, error) {
	xlFile, err := xlsx.OpenFile("download_file.xlsx")
	if err != nil {
		return nil, err
	}
	var sheetNames []string
	for _, sheet := range xlFile.Sheets {
		sheetNames = append(sheetNames, sheet.Name)
	}
	return sheetNames, nil
}

func formatDay(filteredSubjects map[string]map[int]map[int]string, dayMapping map[string]string) string {
	formattedOutput := ""
	for key, value := range filteredSubjects {
		formattedOutput += fmt.Sprintf("%s:\n", key)
		for dayNumber, classes := range value {
			formattedOutput += fmt.Sprintf("%s:\n", dayMapping[fmt.Sprintf("%d", dayNumber)])
			for classKey, classValue := range classes {
				formattedOutput += fmt.Sprintf("  %d. %s\n", classKey, classValue)
			}
			formattedOutput += "\n"
		}
		formattedOutput += "\n"
	}
	return formattedOutput
}

func splitList(inputList []string, chunkSize int) map[int]map[int]string {
	chunks := make(map[int]map[int]string)
	for i := 0; i < len(inputList); i += chunkSize {
		chunk := make(map[int]string)
		for j := 0; j < chunkSize && i+j < len(inputList); j++ {
			chunk[j+1] = inputList[i+j]
		}
		chunks[i/chunkSize+1] = chunk
	}
	return chunks
}

func filterExcelGroup(filePath string, sheetName string) (map[string][]string, error) {
	xlFile, err := xlsx.OpenFile(filePath)
	if err != nil {
		return nil, err
	}
	sheet := xlFile.Sheet[sheetName]
	if sheet == nil {
		return nil, fmt.Errorf("sheet %s not found", sheetName)
	}
	subject1 := "МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б."
	subject2 := "МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б."
	groupResult := make(map[string][]string)
	for _, row := range sheet.Rows {
		for _, cell := range row.Cells {
			text := cell.String()
			if text == subject1 || text == subject2 {
				groupName := row.Cells[0].String()
				groupResult[groupName] = append(groupResult[groupName], text)
			}
		}
	}
	return groupResult, nil
}

func filterExcel(filePath string, sheetName string) (map[string]map[int]map[int]string, error) {
	xlFile, err := xlsx.OpenFile(filePath)
	if err != nil {
		return nil, err
	}
	sheet := xlFile.Sheet[sheetName]
	if sheet == nil {
		return nil, fmt.Errorf("sheet %s not found", sheetName)
	}
	subject1 := "МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б."
	subject2 := "МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б."
	result := make(map[string]map[int]map[int]string)
	groupData, err := filterExcelGroup(filePath, sheetName)
	if err != nil {
		return nil, err
	}
	flag := 0
	for _, row := range sheet.Rows {
		for _, cell := range row.Cells {
			text := cell.String()
			if text == subject1 || text == subject2 {
				scludList := make([]string, len(row.Cells)-1)
				for i, c := range row.Cells[1:] {
					scludList[i] = c.String()
				}
				splitScludList := splitList(scludList, 6)
				if flag < len(groupData) {
					groupName := ""
					for k := range groupData {
						groupName = k
						break
					}
					result[groupName] = splitScludList
					flag++
				}
			}
		}
	}
	return result, nil
}

func filterSubjects(data map[string]map[int]map[int]string, subjects []string) map[string]map[int]map[int]string {
	filteredData := make(map[string]map[int]map[int]string)
	for column, rows := range data {
		for row, cells := range rows {
			for cell, value := range cells {
				for _, subject := range subjects {
					if value == subject {
						if _, ok := filteredData[column]; !ok {
							filteredData[column] = make(map[int]map[int]string)
						}
						if _, ok := filteredData[column][row]; !ok {
							filteredData[column][row] = make(map[int]string)
						}
						filteredData[column][row][cell] = value
					}
				}
			}
		}
	}
	return filteredData
}
