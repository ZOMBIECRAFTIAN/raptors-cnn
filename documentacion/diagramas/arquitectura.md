# Diagramas del Sistema

Esta página contiene los diagramas oficiales del proyecto en formato [Mermaid](https://mermaid.js.org/), que GitHub renderiza automáticamente. Sirven como insumo visual para el README, los capítulos 2-3 de la tesis y las presentaciones a compañeros y comité.

---

## 1. Pipeline completo del sistema

```mermaid
flowchart LR
    A[📷 Imagen<br/>de rapaz<br/>en vuelo] --> B{Pre-procesamiento}
    B --> B1[Resize 224×224]
    B --> B2[Normalización<br/>ImageNet]
    B1 & B2 --> C[🧠 CNN<br/>ResNet-50 / EfficientNet-B3 /<br/>MobileNetV3 / ConvNeXt-Tiny]
    C --> D[Softmax<br/>14 clases]
    D --> E[🏷️ Especie<br/>predicha + prob.]
    C --> F[Grad-CAM]
    F --> G[🔥 Mapa de calor<br/>verificación]
    E --> H[🤟 Video seña<br/>en International Sign]
    E --> I[📋 Ficha técnica<br/>nombre cient. + común]

    style A fill:#FFE5B4
    style C fill:#B4D7FF
    style E fill:#C8E6C9
    style H fill:#F8BBD0
```

---

## 2. Arquitectura modular del proyecto

```mermaid
flowchart TB
    subgraph "📂 Datos"
        D1[datos/raw<br/>imágenes originales]
        D2[datos/processed<br/>train/val/test]
        D3[datos/annotations<br/>metadatos CSV]
    end

    subgraph "🧠 Modelo CNN"
        M1[config.py<br/>14 especies, hiperparámetros]
        M2[data_loader.py<br/>ImageFolder + augmentation]
        M3[model.py<br/>4 arquitecturas]
        M4[train.py<br/>2 etapas: freeze + fine-tune]
        M5[evaluate.py<br/>métricas + ROC + matriz]
        M6[gradcam.py<br/>explicabilidad]
    end

    subgraph "🤟 Módulo Lengua de Señas"
        S1[catalogo_senas/<br/>14 señas en IS]
        S2[glosario_IS_LSM.md<br/>equivalencias]
        S3[videos/<br/>grabaciones]
        S4[instrumentos_validacion/<br/>cuestionario Likert]
    end

    subgraph "📄 Tesis"
        T1[Cap 1 — Introducción]
        T2[Cap 2 — Marco Teórico]
        T3[Cap 3 — Metodología]
        T4[Cap 4 — Resultados]
        T5[Cap 5 — Conclusiones]
    end

    D1 --> D2
    D2 --> M2
    M1 --> M2 & M3 & M4 & M5
    M2 --> M4
    M3 --> M4
    M4 --> M5
    M4 --> M6
    M5 --> T4
    M6 --> T4
    S1 --> S3
    S3 --> S4
    S4 --> T4

    style D1 fill:#FFF9C4
    style M3 fill:#B4D7FF
    style S1 fill:#F8BBD0
    style T4 fill:#C8E6C9
```

---

## 3. Flujo del usuario final (usuaria sorda observando aves)

```mermaid
sequenceDiagram
    actor U as 👤 Usuaria sorda
    participant App as 📱 Aplicación
    participant CNN as 🧠 Modelo CNN
    participant Cat as 📚 Catálogo de señas

    U->>App: Toma foto del cielo
    App->>App: Pre-procesa imagen
    App->>CNN: Imagen 224×224
    CNN->>CNN: Inferencia (~50 ms en GPU)
    CNN-->>App: Predicción: BW · 0.94
    App->>Cat: Solicita seña para BW
    Cat-->>App: Video Buteo platypterus
    App-->>U: Resultado:<br/>📋 Buteo platypterus (Broad-winged Hawk)<br/>🤟 [Video de la seña]<br/>🔥 Grad-CAM verificación
    Note over U: La usuaria aprende<br/>la especie + su seña
```

---

## 4. Estrategia de entrenamiento en dos etapas

```mermaid
flowchart LR
    subgraph "Etapa 1 — Feature Extraction"
        E1A[Cargar pesos<br/>ImageNet]
        E1B[🧊 Congelar<br/>backbone]
        E1C[Entrenar solo<br/>cabeza FC]
        E1D[10 epochs<br/>lr=1e-3, Adam]
    end

    subgraph "Etapa 2 — Fine-Tuning"
        E2A[Descongelar<br/>todo el modelo]
        E2B[Re-entrenar<br/>con lr bajo]
        E2C[60 epochs<br/>lr=1e-4, AdamW<br/>cosine schedule]
        E2D[Mixup + CutMix<br/>+ label smoothing 0.1]
    end

    E1A --> E1B --> E1C --> E1D
    E1D --> E2A
    E2A --> E2B --> E2C --> E2D
    E2D --> Final[💾 best_stage2.pt<br/>modelo final]

    style E1A fill:#B4D7FF
    style E2A fill:#FFC2B4
    style Final fill:#C8E6C9
```

---

## 5. Comparativa PyTorch vs. TensorFlow (objetivo del OE2)

```mermaid
flowchart TB
    Dataset[(Dataset compartido<br/>14 clases × 200 imgs)]

    subgraph "PyTorch (raptors-pt)"
        PT1[torchvision.models]
        PT2[ImageFolder + transforms]
        PT3[Custom train loop]
    end

    subgraph "TensorFlow / Keras (raptors-tf)"
        TF1[tf.keras.applications]
        TF2[image_dataset_from_directory]
        TF3[model.fit + callbacks]
    end

    Dataset --> PT2
    Dataset --> TF2
    PT1 --> PT3
    PT2 --> PT3
    TF1 --> TF3
    TF2 --> TF3

    PT3 --> Compare[📊 Comparativa]
    TF3 --> Compare

    Compare --> M1[Accuracy<br/>F1 macro]
    Compare --> M2[Latencia<br/>de inferencia]
    Compare --> M3[Tiempo total<br/>de entrenamiento]
    Compare --> M4[Facilidad de<br/>despliegue]

    style Dataset fill:#FFF9C4
    style Compare fill:#C8E6C9
```

---

## 6. Las 14 especies — organización taxonómica

```mermaid
flowchart TB
    Order[Accipitriformes<br/>y Falconiformes]

    Order --> F1[Accipitridae<br/>9 especies]
    Order --> F2[Cathartidae<br/>1 especie]
    Order --> F3[Pandionidae<br/>1 especie]
    Order --> F4[Falconidae<br/>3 especies]

    F1 --> SS[SS · Accipiter striatus]
    F1 --> CH[CH · Astur cooperii]
    F1 --> ZT[ZT · Buteo albonotatus]
    F1 --> RT[RT · Buteo jamaicensis]
    F1 --> RS[RS · Buteo lineatus]
    F1 --> BW[BW · Buteo platypterus]
    F1 --> SW[SW · Buteo swainsoni]
    F1 --> NH[NH · Circus hudsonius]
    F1 --> MK[MK · Ictinia mississippiensis]

    F2 --> TV[TV · Cathartes aura]
    F3 --> OS[OS · Pandion haliaetus]
    F4 --> ML[ML · Falco columbarius]
    F4 --> PG[PG · Falco peregrinus]
    F4 --> AK[AK · Falco sparverius]

    style F1 fill:#B4D7FF
    style F2 fill:#FFE5B4
    style F3 fill:#F8BBD0
    style F4 fill:#C8E6C9
```

---

## Uso de estos diagramas

- **Para el README de GitHub**: copiar bloques selectos a la portada del proyecto (GitHub los renderiza automáticamente).
- **Para los capítulos de la tesis**: exportar a PNG con la CLI de Mermaid (`mmdc -i arquitectura.md -o diagrama.png`) o capturas desde mermaid.live.
- **Para presentación a compañeros**: usar el diagrama #1 (pipeline) y #3 (flujo de usuaria sorda) — son los más narrativos y de mayor impacto visual.
