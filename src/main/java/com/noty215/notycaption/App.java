package com.noty215.notycaption;

import com.noty215.notycaption.utils.SettingsManager;
import com.noty215.notycaption.utils.Translator;
import javafx.application.Application;
import javafx.stage.Stage;

/**
 * Application entry point with configuration
 */
public class App extends Application {

    private static App instance;
    private SettingsManager settings;
    private Translator translator;

    @Override
    public void start(Stage primaryStage) {
        instance = this;

        // Initialize settings
        settings = new SettingsManager();
        settings.load();

        // Initialize translator
        translator = new Translator(settings.getLanguage());

        // Launch main window
        Main.main(new String[0]);
    }

    public static App getInstance() {
        return instance;
    }

    public SettingsManager getSettings() {
        return settings;
    }

    public Translator getTranslator() {
        return translator;
    }

    public static void main(String[] args) {
        launch(args);
    }
}