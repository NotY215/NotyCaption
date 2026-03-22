package com.noty215.notycaption;

import com.noty215.notycaption.ui.NotyCaptionWindow;
import com.noty215.notycaption.utils.SettingsManager;
import com.noty215.notycaption.utils.Translator;
import javafx.application.Application;
import javafx.stage.Stage;

/**
 * Main Application Class
 */
public class App extends Application {

    private static NotyCaptionWindow mainWindow;
    private static SettingsManager settings;
    private static Translator translator;

    @Override
    public void start(Stage primaryStage) {
        settings = SettingsManager.getInstance();
        translator = Translator.getInstance(settings.getLanguage());

        mainWindow = new NotyCaptionWindow();
        mainWindow.show(primaryStage);
    }

    public static NotyCaptionWindow getMainWindow() {
        return mainWindow;
    }

    public static SettingsManager getSettings() {
        return settings;
    }

    public static Translator getTranslator() {
        return translator;
    }

    @Override
    public void stop() {
        if (mainWindow != null) {
            mainWindow.saveState();
        }
        settings.save();
    }

    public static void main(String[] args) {
        launch(args);
    }
}