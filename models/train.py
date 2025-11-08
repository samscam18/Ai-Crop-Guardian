
import sys
from pathlib import Path
import tensorflow as tf
from cnn_model import DiseaseDetectionModel
from data_loader import DatasetLoader
import matplotlib.pyplot as plt

class ModelTrainer:
    """Handle model training pipeline"""
    
    def __init__(self, config):
        self.config = config
        self.model = None
        self.history = None
        
    def train(self, data_dir, model_save_path):
        """Complete training pipeline"""
        
        print("=" * 60)
        print("Starting Model Training")
        print("=" * 60)
        
        # Load data
        print("\n[1/5] Loading dataset...")
        loader = DatasetLoader(
            data_dir,
            img_size=self.config.IMG_SIZE,
            batch_size=self.config.BATCH_SIZE
        )
        train_gen, val_gen = loader.load_from_directory()
        
        print(f"Training samples: {train_gen.samples}")
        print(f"Validation samples: {val_gen.samples}")
        print(f"Classes: {len(train_gen.class_indices)}")
        
        # Build model
        print("\n[2/5] Building model...")
        disease_model = DiseaseDetectionModel(
            num_classes=len(train_gen.class_indices),
            img_size=self.config.IMG_SIZE,
            architecture=self.config.MODEL_ARCHITECTURE
        )
        self.model = disease_model.build_model()
        disease_model.compile_model(learning_rate=self.config.LEARNING_RATE)
        
        print(f"Model architecture: {self.config.MODEL_ARCHITECTURE}")
        print(f"Total parameters: {self.model.count_params():,}")
        
        # Train
        print("\n[3/5] Training model...")
        callbacks = disease_model.get_callbacks(model_save_path)
        
        self.history = self.model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=self.config.EPOCHS,
            callbacks=callbacks,
            verbose=1
        )
        
        # Fine-tune
        print("\n[4/5] Fine-tuning model...")
        disease_model.fine_tune(base_layers_to_unfreeze=30)
        
        self.history_fine = self.model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=20,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate
        print("\n[5/5] Evaluating model...")
        results = self.model.evaluate(val_gen)
        print(f"\nFinal Results:")
        print(f"  Loss: {results[0]:.4f}")
        print(f"  Accuracy: {results[1]:.4f}")
        print(f"  Precision: {results[2]:.4f}")
        print(f"  Recall: {results[3]:.4f}")
        
        # Save class indices
        import json
        class_indices_path = Path(model_save_path).parent / 'class_indices.json'
        with open(class_indices_path, 'w') as f:
            json.dump(train_gen.class_indices, f)
        
        print(f"\n✓ Model saved to: {model_save_path}")
        print(f"✓ Class indices saved to: {class_indices_path}")
        
        return self.model, self.history
    
    def plot_training_history(self, save_path='training_history.png'):
        """Plot training metrics"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Accuracy
        axes[0, 0].plot(self.history.history['accuracy'], label='Train')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Val')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(self.history.history['loss'], label='Train')
        axes[0, 1].plot(self.history.history['val_loss'], label='Val')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Precision
        axes[1, 0].plot(self.history.history['precision'], label='Train')
        axes[1, 0].plot(self.history.history['val_precision'], label='Val')
        axes[1, 0].set_title('Model Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Recall
        axes[1, 1].plot(self.history.history['recall'], label='Train')
        axes[1, 1].plot(self.history.history['val_recall'], label='Val')
        axes[1, 1].set_title('Model Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Training history plot saved to: {save_path}")
