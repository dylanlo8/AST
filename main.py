from Whisper import Whisper
from Processor import Processor
from TranslateModel import TranslateModel
from Orchestrator import AudioEmbeddingsDataset, LightningTranslator
import torch
from torch.utils.data import DataLoader
import pandas as pd
import pytorch_lightning as pl

def main():
    # Set up the dataset
    # df1 = pd.read_csv("csv_1.csv")
    df2 = pd.read_csv("csv_2.csv")

    #concatenated_df = pd.concat([df1, df2], ignore_index=True)

    # Parse through AudioProcessor
    processor = Processor()
    train_dataset = processor.process_audio(df2['trimmed_segment_path'], df2['eng_reference'])
    
    # Parse through Whisper Encoder
    torch.cuda.empty_cache()
    whisper = Whisper()
    train_audio_embeddings, train_transcript = whisper.embed_audio(train_dataset)

    # Parse through DataLoader
    train_audiodataset = AudioEmbeddingsDataset(train_audio_embeddings, train_transcript)
    train_audioloader = DataLoader(train_audiodataset, batch_size=2, shuffle=True)

    torch.cuda.empty_cache()
    lightning_translator = LightningTranslator()

    # for batch in train_audioloader:
    #     audio_embeddings = batch[0].to("cuda") # Extract the audio embeddings from the batch
    #     transcript = batch[1]
    #     output = lightning_translator.forward(audio_embeddings)


    # print(lightning_translator.calculate_loss(output.logits, transcript))

    # print(lightning_translator.model.decode(output)) # generated
    # print(lightning_translator.model.tokenizer.batch_decode(transcript))
    trainer = pl.Trainer(devices = 1, accelerator= 'auto')
    trainer.fit(model=lightning_translator, train_dataloaders=train_audioloader)

if __name__ == "__main__":
    main()
