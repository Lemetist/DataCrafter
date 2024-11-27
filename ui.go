package main

import (
	"fmt"
	"os"
	"github.com/andlabs/ui"
	"encoding/json"
	"io/ioutil"
)

type App struct {
	window       *ui.Window
	textOutput   *ui.MultilineEntry
	statusBar    *ui.Label
	comboBox     *ui.Combobox
	nameSheet    string
}

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

func (app *App) initUI() {
	app.window = ui.NewWindow("SusMan -- Neon_Leonov", 400, 300, true)
	app.window.OnClosing(func(*ui.Window) bool {
		ui.Quit()
		return true
	})

	vbox := ui.NewVerticalBox()
	vbox.SetPadded(true)
	app.window.SetChild(vbox)

	app.textOutput = ui.NewMultilineEntry()
	app.textOutput.SetReadOnly(true)
	vbox.Append(app.textOutput, true)

	buttonBox := ui.NewHorizontalBox()
	buttonBox.SetPadded(true)
	vbox.Append(buttonBox, false)

	addButton := ui.NewButton("Добавить")
	addButton.OnClicked(func(*ui.Button) {
		app.handleButtonClick("Добавить")
	})
	buttonBox.Append(addButton, false)

	clearButton := ui.NewButton("Очистить")
	clearButton.OnClicked(func(*ui.Button) {
		app.textOutput.SetText("")
		app.statusBar.SetText("Текст очищен.")
	})
	buttonBox.Append(clearButton, false)

	settingsButton := ui.NewButton("Настройки")
	settingsButton.OnClicked(func(*ui.Button) {
		app.openSettingsDialog()
	})
	buttonBox.Append(settingsButton, false)

	app.statusBar = ui.NewLabel("")
	vbox.Append(app.statusBar, false)

	app.comboBox = ui.NewCombobox()
	app.comboBox.OnSelected(func(*ui.Combobox) {
		app.onDaySelected(app.comboBox.Selected())
	})
	vbox.Append(app.comboBox, false)
}

func (app *App) handleButtonClick(text string) {
	if text == "Добавить" {
		app.loadFilteredData()
	}
}

func (app *App) loadDays() {
	days := []string{"Понедельник", "Вторник", "Среда"} // Mock data
	for _, day := range days {
		app.comboBox.Append(day)
	}
}

func (app *App) onDaySelected(index int) {
	selectedDay := app.comboBox.SelectedText()
	app.statusBar.SetText(fmt.Sprintf("Расписание: %s", selectedDay))
	app.nameSheet = selectedDay
}

func (app *App) loadFilteredData() {
	data, err := ioutil.ReadFile("result.json")
	if err != nil {
		app.statusBar.SetText("Файл result.json не найден.")
		return
	}

	var filteredSubjects map[string]map[int]map[int]string
	err = json.Unmarshal(data, &filteredSubjects)
	if err != nil {
		app.statusBar.SetText("Ошибка при чтении файла result.json.")
		return
	}

	app.textOutput.SetText("")
	for group, days := range filteredSubjects {
		app.textOutput.Append(fmt.Sprintf("%s:\n", group))
		for day, classes := range days {
			app.textOutput.Append(fmt.Sprintf("  День %d:\n", day))
			for classNum, className := range classes {
				app.textOutput.Append(fmt.Sprintf("    %d. %s\n", classNum, className))
			}
		}
	}
	app.statusBar.SetText("Фильтрованные данные добавлены в текстовое поле.")
}

func (app *App) openSettingsDialog() {
	// Placeholder for settings dialog
}
