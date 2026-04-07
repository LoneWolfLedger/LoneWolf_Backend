import torch, torch.nn as nn, numpy as np
class LiquidMicroKAN(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.spline_adapter = nn.Linear(input_dim, 16)
        self.liquid_activation = nn.SiLU()
        self.state_decoder = nn.Linear(16, 1)
    def forward(self, x): 
        return self.state_decoder(self.liquid_activation(self.spline_adapter(x)))

def synthesize_prediction(X_matrix, y_target, current_price, epochs=20):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    X_t = torch.tensor(X_matrix, dtype=torch.float32).to(device)
    y_t = torch.tensor(y_target, dtype=torch.float32).unsqueeze(1).to(device)
    model = LiquidMicroKAN(X_t.shape[1]).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)
    model.train()
    for _ in range(epochs): 
        optimizer.zero_grad()
        loss = nn.HuberLoss()(model(X_t), y_t)
        loss.backward(); optimizer.step()
    last_state = torch.tensor(X_matrix[-1:], dtype=torch.float32).to(device)
    return model(last_state).item()
