import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const NAMENODE_URL = "http://localhost:8000";

function FileBrowser({ files, selectedFile, onSelect }) {
  return (
    <div className="file-browser">
      <div className="panel-header">
        <br/>
        <h2>Stored Files</h2>
        <p className="panel-sub">Click a file to visualize its blocks</p>
      </div>
      <div className="file-list">
        {files.length === 0 ? (
          <div className="empty-state">
            No files stored yet.<br />Use the CLI to <code>put</code> a file.
          </div>
        ) : (
          files.map((file) => (
            <div
              key={file.id}
              className={`file-card ${selectedFile?.id === file.id ? "selected" : ""}`}
              onClick={() => onSelect(file)}
            >
              <div className="file-icon">📁</div>
              <div className="file-meta">
                <span className="file-name">{file.name}</span>
                <span className="file-path">{file.path}</span>
                <div className="file-tags">
                  <span className="tag">ID: {file.id}</span>
                  <span className="tag">{(file.size / 1024).toFixed(2)} KB</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

function BlockVisualizer({ file, blocks }) {
  if (!file) {
    return (
      <div className="visualizer empty-visualizer">
        <div className="visualizer-placeholder">
          <div className="placeholder-icon">⬡</div>
          <p>Select a file to see how its blocks are distributed across DataNodes</p>
        </div>
      </div>
    );
  }

  // Group blocks by datanode
  const datanodeMap = {};
  blocks.forEach((block) => {
    const key = `${block.datanode_ip}:${block.datanode_port}`;
    if (!datanodeMap[key]) datanodeMap[key] = [];
    datanodeMap[key].push(block);
  });

  const datanodes = Object.entries(datanodeMap);

  return (
    <div className="visualizer">
      <div className="panel-header">
        <span className="panel-eyebrow">Block Map</span>
        <h2>{file.name}</h2>
        <p className="panel-sub">
          {blocks.length} block{blocks.length !== 1 ? "s" : ""} across {datanodes.length} DataNode{datanodes.length !== 1 ? "s" : ""}
          <br/>
          <span className="disclaimer"> Empty DataNodes not shown</span>
        </p>
      </div>

      <div className="file-source">
        <div className="source-box">
          <span className="source-label">FILE</span>
          <span className="source-name">{file.name}</span>
          <span className="source-size">{(file.size / 1024).toFixed(2)} KB</span>
        </div>
        <div className="flow-arrow">↓</div>
        <span className="flow-label">split into {blocks.length} block{blocks.length !== 1 ? "s" : ""}</span>
        <div className="flow-arrow">↓</div>
      </div>

      <div className="datanode-grid">
        {datanodes.map(([key, dnBlocks], i) => (
          <div key={key} className="datanode-card" style={{ animationDelay: `${i * 0.1}s` }}>
            <div className="datanode-header">
              <span className="datanode-icon">🖥</span>
              <div>
                <span className="datanode-label">DataNode {i + 1}</span>
                <span className="datanode-address">{key}</span>
              </div>
            </div>
            <div className="blocks-container">
              {dnBlocks.map((block, j) => (
                <div
                  key={block.block_id}
                  className="block-chip"
                  style={{ animationDelay: `${i * 0.1 + j * 0.05}s` }}
                >
                  <span className="block-label">Block</span>
                  <span className="block-id">#{block.block_id}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [blocks, setBlocks] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get(`${NAMENODE_URL}/files`)
      .then((res) => setFiles(res.data))
      .catch(() => setFiles([]));
  }, []);

  const handleSelectFile = (file) => {
    setSelectedFile(file);
    setLoading(true);
    axios.get(`${NAMENODE_URL}/files/${file.id}`)
      .then((res) => {
        setBlocks(res.data);
        setLoading(false);
      })
      .catch(() => {
        setBlocks([]);
        setLoading(false);
      });
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">⬡</span>
            <span className="logo-text">mini<strong>HDFS</strong></span>
          </div>
          <span className="header-tagline"> Visual Dashboard</span>
        </div>
      </header>

      <main className="app-main">
        <FileBrowser
          files={files}
          selectedFile={selectedFile}
          onSelect={handleSelectFile}
        />
        {loading ? (
          <div className="visualizer empty-visualizer">
            <div className="visualizer-placeholder">
              <div className="placeholder-icon spinning">⬡</div>
              <p>Loading blocks...</p>
            </div>
          </div>
        ) : (
          <BlockVisualizer file={selectedFile} blocks={blocks} />
        )}
      </main>
    </div>
  );
}