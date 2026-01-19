import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, Link as LinkIcon, CheckCircle2 } from 'lucide-react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Input } from './ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HomePage = ({ onVerificationComplete }) => {
  const [inputType, setInputType] = useState('text');
  const [textContent, setTextContent] = useState('');
  const [urlContent, setUrlContent] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async () => {
    setError(null);
    setIsLoading(true);

    try {
      let content = '';
      let type = inputType;

      if (inputType === 'text') {
        if (!textContent.trim()) {
          setError('Please enter some text to verify');
          setIsLoading(false);
          return;
        }
        content = textContent;
      } else if (inputType === 'url') {
        if (!urlContent.trim()) {
          setError('Please enter a URL to verify');
          setIsLoading(false);
          return;
        }
        content = urlContent;
      } else if (inputType === 'image') {
        if (!imagePreview) {
          setError('Please upload an image');
          setIsLoading(false);
          return;
        }
        content = imagePreview;
      }

      const response = await axios.post(`${API}/verify`, {
        input_type: type,
        content: content
      });

      onVerificationComplete(response.data);

    } catch (err) {
      console.error('Verification error:', err);
      setError(err.response?.data?.detail || 'Verification failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 noise-bg">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-blue-900 text-white">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1654262609484-76d1a8f3b016?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwxfHxpbmRpYW4lMjBqb3VybmFsaXN0JTIwd29ya2luZyUyMGxhcHRvcHxlbnwwfHx8fDE3Njg4MjY2NzF8MA&ixlib=rb-4.1.0&q=85')`,
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }}></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h1 className="font-serif font-black tracking-tight text-5xl md:text-7xl leading-[0.9] mb-8">
              SATYA-VERIFY
            </h1>
            <p className="font-sans text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto mb-12 leading-relaxed">
              AI-powered fact-checking for Indian regional news. Verify claims in seconds across Hindi, Tamil, Telugu, Bengali, and more.
            </p>
            
            {/* Trust Indicators */}
            <div className="flex flex-wrap justify-center gap-6 text-sm font-mono uppercase tracking-wider">
              <div className="flex items-center gap-2" data-testid="trust-indicator-sources">
                <CheckCircle2 className="w-5 h-5" />
                <span>8+ Trusted Sources</span>
              </div>
              <div className="flex items-center gap-2" data-testid="trust-indicator-languages">
                <CheckCircle2 className="w-5 h-5" />
                <span>7 Indian Languages</span>
              </div>
              <div className="flex items-center gap-2" data-testid="trust-indicator-ai">
                <CheckCircle2 className="w-5 h-5" />
                <span>OpenAI GPT-5.2</span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Input Section */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 -mt-12 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="bg-white rounded-xl shadow-[0_20px_50px_rgba(0,0,0,0.1)] p-8 md:p-12 border border-slate-200"
          data-testid="verification-input-card"
        >
          <h2 className="font-serif font-bold text-3xl md:text-4xl mb-6 text-slate-900">
            Verify Content
          </h2>
          
          <Tabs value={inputType} onValueChange={setInputType} className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-8" data-testid="input-type-tabs">
              <TabsTrigger value="text" className="flex items-center gap-2" data-testid="tab-text">
                <FileText className="w-4 h-4" />
                Text
              </TabsTrigger>
              <TabsTrigger value="url" className="flex items-center gap-2" data-testid="tab-url">
                <LinkIcon className="w-4 h-4" />
                URL
              </TabsTrigger>
              <TabsTrigger value="image" className="flex items-center gap-2" data-testid="tab-image">
                <Upload className="w-4 h-4" />
                Image
              </TabsTrigger>
            </TabsList>

            <TabsContent value="text" data-testid="text-input-content">
              <Textarea
                data-testid="text-input"
                placeholder="Paste news text, WhatsApp forward, or any claim to verify..."
                className="min-h-[200px] text-lg border-2 focus:border-blue-900 rounded-lg"
                value={textContent}
                onChange={(e) => setTextContent(e.target.value)}
              />
            </TabsContent>

            <TabsContent value="url" data-testid="url-input-content">
              <Input
                data-testid="url-input"
                type="url"
                placeholder="https://example.com/news-article"
                className="text-lg border-2 focus:border-blue-900 rounded-lg h-14"
                value={urlContent}
                onChange={(e) => setUrlContent(e.target.value)}
              />
              <p className="text-sm text-slate-500 mt-3 font-mono">
                Enter the URL of a news article or social media post
              </p>
            </TabsContent>

            <TabsContent value="image" data-testid="image-input-content">
              <div className="border-2 border-dashed border-slate-300 rounded-lg p-8 text-center hover:border-blue-900 transition-colors">
                {imagePreview ? (
                  <div data-testid="image-preview">
                    <img
                      src={imagePreview}
                      alt="Uploaded content"
                      className="max-h-64 mx-auto rounded-lg mb-4"
                    />
                    <Button
                      data-testid="change-image-button"
                      variant="outline"
                      onClick={() => {
                        setImageFile(null);
                        setImagePreview(null);
                      }}
                      className="rounded-none border-2"
                    >
                      Change Image
                    </Button>
                  </div>
                ) : (
                  <label className="cursor-pointer">
                    <Upload className="w-12 h-12 mx-auto mb-4 text-slate-400" />
                    <p className="text-lg font-semibold mb-2">Upload Screenshot</p>
                    <p className="text-sm text-slate-500 font-mono">
                      JPG, PNG, or WEBP up to 10MB
                    </p>
                    <input
                      data-testid="image-upload-input"
                      type="file"
                      accept="image/jpeg,image/png,image/webp"
                      className="hidden"
                      onChange={handleImageUpload}
                    />
                  </label>
                )}
              </div>
            </TabsContent>
          </Tabs>

          {error && (
            <div className="mt-6 p-4 bg-rose-50 border border-rose-200 rounded-lg" data-testid="error-message">
              <p className="text-rose-700 font-medium">{error}</p>
            </div>
          )}

          <Button
            data-testid="verify-button"
            onClick={handleSubmit}
            disabled={isLoading}
            className="w-full mt-8 bg-blue-900 text-white hover:bg-blue-800 rounded-none px-8 py-6 text-lg font-bold tracking-wide shadow-lg hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-3">
                <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></div>
                Verifying...
              </span>
            ) : (
              'VERIFY NOW'
            )}
          </Button>
        </motion.div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm hover-lift"
            data-testid="feature-multilingual"
          >
            <h3 className="font-sans font-semibold text-xl mb-3 uppercase">Multilingual Support</h3>
            <p className="text-slate-600 leading-relaxed">
              Verify content in Hindi, Tamil, Telugu, Bengali, Kannada, Malayalam, Marathi, and English.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm hover-lift"
            data-testid="feature-trusted-sources"
          >
            <h3 className="font-sans font-semibold text-xl mb-3 uppercase">Trusted Sources</h3>
            <p className="text-slate-600 leading-relaxed">
              Cross-checks against PIB Fact Check, Alt News, BoomLive, The Hindu, PTI, and government portals.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm hover-lift"
            data-testid="feature-explainable"
          >
            <h3 className="font-sans font-semibold text-xl mb-3 uppercase">Explainable AI</h3>
            <p className="text-slate-600 leading-relaxed">
              Every verdict comes with detailed explanations and clickable source citations.
            </p>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
