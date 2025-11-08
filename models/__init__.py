class DiseasePredictor:
    """Handle disease prediction from images"""
    
    def __init__(self, model_path, class_indices_path, img_size=(224, 224)):
        # ✅ Fix: allow legacy HDF5 models to load
        self.model = load_model(model_path, compile=False, safe_mode=False)
        self.img_size = img_size
        
        # Load class indices
        with open(class_indices_path, 'r') as f:
            self.class_indices = json.load(f)
        
        # Reverse mapping
        self.index_to_class = {v: k for k, v in self.class_indices.items()}
