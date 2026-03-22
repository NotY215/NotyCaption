package com.noty215.notycaption;

import com.noty215.notycaption.ui.NotyCaptionWindow;
import com.noty215.notycaption.utils.SingleInstance;
import com.noty215.notycaption.utils.ResourcePath;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Main entry point for NotyCaption Pro
 * Version: 2026.5.0
 */
public class Main extends Application {

    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static final String APP_NAME = "NotyCaption Pro";
    private static final String APP_VERSION = "2026.5.0";
    private static final String APP_AUTHOR = "NotY215";

    private static Stage primaryStage;
    private static NotyCaptionWindow mainWindow;

    @Override
    public void init() throws Exception {
        super.init();

        // Setup logging directory
        setupLogging();

        logger.info("=" .repeat(80));
        logger.info("NotyCaption Pro Launch - Version {}", APP_VERSION);
        logger.info("=" .repeat(80));
        logger.info("Java version: {}", System.getProperty("java.version"));
        logger.info("Platform: {} {}", System.getProperty("os.name"), System.getProperty("os.arch"));
        logger.info("Working directory: {}", System.getProperty("user.dir"));
    }

    @Override
    public void start(Stage stage) {
        primaryStage = stage;

        // Check for single instance
        if (SingleInstance.isAlreadyRunning()) {
            logger.warn("Another instance is already running");
            Platform.exit();
            return;
        }

        // Create splash screen
        SplashScreen splash = new SplashScreen();
        splash.show();

        // Initialize main window in background
        new Thread(() -> {
            try {
                Thread.sleep(1000);

                Platform.runLater(() -> {
                    try {
                        mainWindow = new NotyCaptionWindow();
                        mainWindow.show();
                        splash.hide();

                        primaryStage = mainWindow.getStage();
                        primaryStage.setOnCloseRequest(event -> {
                            mainWindow.close();
                            SingleInstance.release();
                        });

                        logger.info("Main window initialized");
                    } catch (Exception e) {
                        logger.error("Failed to initialize main window", e);
                        splash.hide();
                        Platform.exit();
                    }
                });
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                splash.hide();
            }
        }).start();
    }

    @Override
    public void stop() throws Exception {
        logger.info("Application shutting down");
        if (mainWindow != null) {
            mainWindow.cleanupBeforeExit();
        }
        SingleInstance.release();
        logger.info("=" .repeat(80));
        logger.info("NotyCaption Pro Secure Shutdown");
        logger.info("=" .repeat(80));
        super.stop();
    }

    private void setupLogging() throws IOException {
        String baseDir = System.getProperty("user.dir");
        String logDir = baseDir + File.separator + "logs";
        Files.createDirectories(Paths.get(logDir));

        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm-ss.SSS"));
        String logFile = logDir + File.separator + "NotyCaption_" + timestamp + ".log";

        System.setProperty("org.slf4j.simpleLogger.logFile", logFile);
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "info");
        System.setProperty("org.slf4j.simpleLogger.showDateTime", "true");
        System.setProperty("org.slf4j.simpleLogger.dateTimeFormat", "yyyy-MM-dd HH:mm:ss.SSS");
    }

    public static Stage getPrimaryStage() {
        return primaryStage;
    }

    public static NotyCaptionWindow getMainWindow() {
        return mainWindow;
    }

    public static void main(String[] args) {
        launch(args);
    }

    /**
     * Simple splash screen implementation
     */
    private static class SplashScreen {
        private Stage splashStage;

        public void show() {
            splashStage = new Stage(StageStyle.TRANSPARENT);
            splashStage.initStyle(StageStyle.TRANSPARENT);

            javafx.scene.Scene scene = new javafx.scene.Scene(createSplashContent());
            scene.setFill(javafx.scene.paint.Color.TRANSPARENT);

            splashStage.setScene(scene);
            splashStage.centerOnScreen();
            splashStage.show();
        }

        private javafx.scene.Parent createSplashContent() {
            javafx.scene.layout.VBox vbox = new javafx.scene.layout.VBox();
            vbox.setAlignment(javafx.geometry.Pos.CENTER);
            vbox.setStyle("-fx-background-color: #1a1a2e; -fx-background-radius: 20;");
            vbox.setPrefSize(600, 400);

            javafx.scene.control.Label title = new javafx.scene.control.Label(APP_NAME);
            title.setStyle("-fx-text-fill: #89b4fa; -fx-font-size: 36px; -fx-font-weight: bold;");

            javafx.scene.control.Label subtitle = new javafx.scene.control.Label("AI-Powered Caption Generator");
            subtitle.setStyle("-fx-text-fill: #cdd6f5; -fx-font-size: 18px;");

            javafx.scene.control.Label version = new javafx.scene.control.Label("Version " + APP_VERSION);
            version.setStyle("-fx-text-fill: #a6e3a1; -fx-font-size: 14px;");

            javafx.scene.control.ProgressIndicator progress = new javafx.scene.control.ProgressIndicator();
            progress.setStyle("-fx-progress-color: #89b4fa;");

            vbox.getChildren().addAll(title, subtitle, version, progress);
            vbox.setSpacing(20);

            return vbox;
        }

        public void hide() {
            if (splashStage != null) {
                splashStage.hide();
            }
        }
    }
}