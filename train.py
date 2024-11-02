import time
import torch

def train(model, train_loader, criterion, optimizer, device, epoch, num_epochs):
    model.train()
    running_loss = 0.0
    running_corrects = 0
    total_samples = 0
    start_time = time.time()

    for i, (images, targets) in enumerate(train_loader, 1):
        images, targets = images.to(device), targets.to(device)

        outputs = model(images)
        loss = criterion(outputs, targets.squeeze(1).long())
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        
        # Accuracy calculation
        _, preds = torch.max(outputs, dim=1)
        running_corrects += torch.sum(preds == targets.squeeze(1))
        total_samples += targets.size(0)
        
        if i % 10 == 0:
            elapsed_time = time.time() - start_time
            avg_time_per_batch = elapsed_time / i
            remaining_batches = len(train_loader) - i
            eta = avg_time_per_batch * remaining_batches
            batch_accuracy = (running_corrects / total_samples).item() * 100

            print(f"Epoch [{epoch+1}/{num_epochs}], Batch [{i}/{len(train_loader)}], "
                  f"Loss: {loss.item():.4f}, Accuracy: {batch_accuracy:.2f}%, ETA: {eta:.2f} seconds")

    epoch_loss = running_loss / len(train_loader)
    epoch_accuracy = (running_corrects / total_samples).item() * 100
    total_time = time.time() - start_time
    print(f"Epoch [{epoch+1}/{num_epochs}] complete. Average Loss: {epoch_loss:.4f}, "
          f"Average Accuracy: {epoch_accuracy:.2f}%, Time Taken: {total_time:.2f} seconds")
    
    return epoch_loss, epoch_accuracy
