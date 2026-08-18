import torch
import torch.nn as nn
import torch.nn.functional as F

class BasicSelfAttention(nn.Module):
    """
    A basic implementation of the Scaled Dot-Product Self-Attention mechanism
    introduced in the Transformer architecture.
    """
    def __init__(self, embed_size):
        super(BasicSelfAttention, self).__init__()
        self.embed_size = embed_size
        
        # Linear transformations for Queries, Keys, and Values
        self.query = nn.Linear(embed_size, embed_size)
        self.key = nn.Linear(embed_size, embed_size)
        self.value = nn.Linear(embed_size, embed_size)

    def forward(self, x):
        # x shape: (batch_size, sequence_length, embed_size)
        
        # 1. Compute Q, K, V
        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)
        
        # 2. Compute attention scores (Q * K^T)
        # We transpose the last two dimensions of K to compute the dot product
        attention_scores = torch.matmul(Q, K.transpose(-2, -1))
        
        # 3. Scale the scores
        # Scaling prevents the softmax gradients from vanishing
        attention_scores = attention_scores / (self.embed_size ** 0.5)
        
        # 4. Apply softmax to get attention weights
        # Softmax makes the scores across the sequence length sum to 1
        attention_weights = F.softmax(attention_scores, dim=-1)
        
        # 5. Multiply weights by Values (Attention * V)
        out = torch.matmul(attention_weights, V)
        
        return out, attention_weights

if __name__ == "__main__":
    # Example Usage
    batch_size = 1
    sequence_length = 5
    embed_size = 8
    
    # Create a dummy input (e.g., 5 words, each represented by a vector of size 8)
    dummy_input = torch.rand((batch_size, sequence_length, embed_size))
    
    print("Input shape:", dummy_input.shape)
    
    # Initialize the self-attention layer
    attention_layer = BasicSelfAttention(embed_size)
    
    # Pass the input through the layer
    output, weights = attention_layer(dummy_input)
    
    print("\nOutput shape:", output.shape)
    print("Attention Weights shape:", weights.shape)
    print("\nAttention Weights (showing how much each token attends to others):")
    print(weights)
