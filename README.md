# 🛡️ AI-Based Network Intrusion Detection System (NIDS)

A complete Deep Learning based Network Intrusion Detection System built using:

- ✅ Autoencoder (Deep Learning)
- ✅ 90% Benign + 10% Attack Dataset
- ✅ Offline Traffic Replay Testing
- ✅ Real-time Streamlit Dashboard
- ✅ Anomaly vs Normal Detection
- ✅ Live Counters & Metrics

---

# Project Overview

This project detects malicious network traffic using an **Unsupervised deep learning Autoencoder model**.

Instead of training on attack data, the model is trained only on **normal (benign) traffic**, and it detects anomalies based on reconstruction error.

---

# How It Works

1. Train Autoencoder on normal traffic
2. Calculate reconstruction error
3. Set threshold using 95th percentile
4. During testing:
   - If error > threshold → 🚨 Attack
   - If error ≤ threshold → ✅ Normal

---

# Dataset Details

We generated a synthethic test dataset:

- **Total Rows:** 500
- **Benign Traffic:** ~ 450
- **Attack Traffic:** ~ 50

---

# Why this ratio for Attack dataset?

Real-world traffic mostly contains normal packets.

This distribution helps simulate realistic network behavior.

---

# Why Autoencoder?

- Works without labeled attack data
- Learns normal behavior patterns
- Detects unknown attacks
- Useful for zero-day detection

---

# Requirements

Typical libraries used:

```
tensorflow
numpy
pandas
scikit-learn
streamlit
joblib
matplotlib
seaborn
```

---

# Future Improvements

- Real packet capture using Scapy
- Real-time IDS deployment
- Docker containerization
- Integration with firewall
- Alert system via email
- Cloud deployment

---

# Final Output

When running dashboard:

You will see:

- Total Packets: 500
- Normal Traffic
- Anomaly Traffic
- Replay stops automatically after completion

---

# 👨‍💻 Developer

- **Taha Imran**
- **Email**: tahaimran315@gmail.com -- [Email Me](mailto:tahaimran315@gmail.com)
- **LinkedIn**: www.linkedin.com/in/taha-imran-9a6987338 -- [Taha Imran](www.linkedin.com/in/taha-imran-9a6987338)

Built using:
- Python
- TensorFlow
- Streamlit

---

# Conclusion

This project demonstrates:

- Practical anomaly detection
- Deep learning for cybersecurity
- Real-time monitoring dashboard
- Production-ready threshold logic

This is a strong base for building a real NIDS system.

---

# 🤝 **Contributing**
Feel free to fork the repo, suggest improvements, or raise issues. All contributions are welcome!
