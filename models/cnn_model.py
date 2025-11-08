import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50, VGG16, MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

class DiseaseDetectionModel:
    """CNN model for crop disease detection"""
    
    def __init__(self, num_classes, img_size=(224, 224), architecture='resnet50'):
        self.num_classes = num_classes
        self.img_size = img_size + (3,)
        self.architecture = architecture
        self.model = None
        
    def build_model(self):
        """Build CNN model with transfer learning"""
        
        # Base model selection
        if self.architecture == 'resnet50':
            base_model = ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=self.img_size
            )
        elif self.architecture == 'vgg16':
            base_model = VGG16(
                weights='imagenet',
                include_top=False,
                input_shape=self.img_size
            )
        elif self.architecture == 'mobilenet':
            base_model = MobileNetV2(
                weights='imagenet',
                include_top=False,
                input_shape=self.img_size
            )
        else:
            raise ValueError(f"Unknown architecture: {self.architecture}")
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Build full model
        inputs = layers.Input(shape=self.img_size)
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(512, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        self.model = models.Model(inputs, outputs)
        
        return self.model
    
    def compile_model(self, learning_rate=0.001):
        """Compile the model"""
        self.model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )
    
    def get_callbacks(self, model_path):
        """Get training callbacks"""
        callbacks = [
            ModelCheckpoint(
                model_path,
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        return callbacks
    
    def fine_tune(self, base_layers_to_unfreeze=30):
        """Fine-tune the model by unfreezing some base layers"""
        base_model = self.model.layers[1]
        base_model.trainable = True
        
        # Freeze all layers except the last N
        for layer in base_model.layers[:-base_layers_to_unfreeze]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.compile_model(learning_rate=1e-5)

