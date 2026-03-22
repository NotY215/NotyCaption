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
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * NotyCaption Pro - Professional AI Caption Generator
 * Version: 2026.5.0
 * Author: NotY215
 */
public class Main extends Application {

    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static NotyCaptionWindow window;
    private static SingleInstance instance;

    public static void main(String[] args) {
        // Check for single instance
        instance = new SingleInstance();
        if (instance.isAlreadyRunning()) {
            logger.warn("Duplicate instance detected");
            System.err.println("NotyCaption is already open in another window.");
            System.exit(1);
            return;
        }

        // Setup logging
        setupLogging();

        // Launch JavaFX application
        launch(args);
    }

    private static void setupLogging() {
        try {
            String baseDir = System.getProperty("user.dir");
            File logDir = new File(baseDir, "logs");
            if (!logDir.exists()) {
                logDir.mkdirs();
            }

            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm-ss.SSS"));
            File logFile = new File(logDir, "NotyCaption_" + timestamp + ".log");

            System.setProperty("org.slf4j.simpleLogger.logFile", logFile.getAbsolutePath());
            System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "info");

            logger.info("=" .repeat(80));
            logger.info("NotyCaption Pro Launch - Version 2026.5.0");
            logger.info("=" .repeat(80));
            logger.info("Java version: " + System.getProperty("java.version"));
            logger.info("Platform: " + System.getProperty("os.name") + " " + System.getProperty("os.arch"));
            logger.info("Working directory: " + System.getProperty("user.dir"));
            logger.info("Log file: " + logFile.getAbsolutePath());
        } catch (Exception e) {
            System.err.println("Failed to setup logging: " + e.getMessage());
        }
    }

    @Override
    public void start(Stage primaryStage) {
        // Create splash screen
        SplashScreen splash = new SplashScreen();
        splash.show();

        // Initialize application in background
        new Thread(() -> {
            try {
                // Load settings
                window = new NotyCaptionWindow();

                Platform.runLater(() -> {
                    splash.close();
                    window.show(primaryStage);
                });
            } catch (Exception e) {
                logger.error("Failed to initialize application", e);
                Platform.runLater(() -> {
                    splash.close();
                    javafx.scene.control.Alert alert = new javafx.scene.control.Alert(
                            javafx.scene.control.Alert.AlertType.ERROR,
                            "Failed to initialize application: " + e.getMessage()
                    );
                    alert.showAndWait();
                    Platform.exit();
                });
            }
        }).start();
    }

    @Override
    public void stop() {
        if (window != null) {
            window.close();
        }
        instance.release();
        logger.info("=" .repeat(80));
        logger.info("NotyCaption Pro Secure Shutdown");
        logger.info("=" .repeat(80));
    }

    private static class SplashScreen {
        private javafx.stage.Stage stage;

        public void show() {
            stage = new javafx.stage.Stage();
            stage.initStyle(StageStyle.TRANSPARENT);

            javafx.scene.layout.VBox root = new javafx.scene.layout.VBox();
            root.setStyle("-fx-background-color: #1a1a2e; -fx-border-radius: 15; -fx-background-radius: 15;");
            root.setAlignment(javafx.geometry.Pos.CENTER);
            root.setPrefSize(600, 400);

            javafx.scene.text.Text title = new javafx.scene.text.Text("NotyCaption Pro");
            title.setStyle("-fx-font-size: 36px; -fx-font-weight: bold; -fx-fill: #89b4fa;");
            root.getChildren().add(title);

            javafx.scene.text.Text subtitle = new javafx.scene.text.Text("Professional AI Caption Generator");
            subtitle.setStyle("-fx-font-size: 14px; -fx-fill: #e0e0ff;");
            root.getChildren().add(subtitle);

            javafx.scene.control.ProgressBar progress = new javafx.scene.control.ProgressBar();
            progress.setPrefWidth(400);
            progress.setStyle("-fx-accent: #89b4fa;");
            javafx.scene.layout.VBox.setMargin(progress, new javafx.geometry.Insets(30, 0, 0, 0));
            root.getChildren().add(progress);

            javafx.scene.text.Text status = new javafx.scene.text.Text("Initializing...");
            status.setStyle("-fx-font-size: 12px; -fx-fill: #a6e3a1;");
            javafx.scene.layout.VBox.setMargin(status, new javafx.geometry.Insets(15, 0, 0, 0));
            root.getChildren().add(status);

            javafx.scene.Scene scene = new javafx.scene.Scene(root);
            scene.setFill(javafx.scene.paint.Color.TRANSPARENT);
            stage.setScene(scene);
            stage.centerOnScreen();
            stage.show();

            // Animate progress
            new Thread(() -> {
                for (int i = 0; i <= 100; i++) {
                    final int value = i;
                    Platform.runLater(() -> progress.setProgress(value / 100.0));
                    try {
                        Thread.sleep(20);
                    } catch (InterruptedException e) {
                        break;
                    }
                }
                Platform.runLater(() -> status.setText("Ready"));
            }).start();
        }

        public void close() {
            if (stage != null) {
                stage.close();
            }
        }
    }
}