import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, AlertTriangle, HelpCircle, ExternalLink, ArrowLeft, Shield } from 'lucide-react';
import { Button } from './ui/button';
import { Progress } from './ui/progress';

const ResultsPage = ({ results, onBack }) => {
  if (!results) return null;

  const getVerdictIcon = (verdict) => {
    switch (verdict) {
      case 'TRUE':
        return <CheckCircle2 className="w-12 h-12" />;
      case 'FALSE':
        return <XCircle className="w-12 h-12" />;
      case 'MISLEADING':
        return <AlertTriangle className="w-12 h-12" />;
      default:
        return <HelpCircle className="w-12 h-12" />;
    }
  };

  const getVerdictStyles = (verdict) => {
    switch (verdict) {
      case 'TRUE':
        return 'text-emerald-700 bg-emerald-50 border-emerald-200';
      case 'FALSE':
        return 'text-rose-700 bg-rose-50 border-rose-200';
      case 'MISLEADING':
        return 'text-orange-700 bg-orange-50 border-orange-200';
      default:
        return 'text-slate-600 bg-slate-100 border-slate-200';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 75) return 'bg-emerald-600';
    if (confidence >= 50) return 'bg-orange-500';
    return 'bg-slate-400';
  };

  return (
    <div className="min-h-screen bg-slate-50 noise-bg">
      {/* Header */}
      <div className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Button
            data-testid="back-button"
            onClick={onBack}
            variant="ghost"
            className="mb-4 text-slate-600 hover:text-blue-900 rounded-md"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Verification
          </Button>
          
          <div className="flex items-start gap-4">
            <div className="flex-1">
              <h1 className="font-serif font-bold text-3xl md:text-5xl mb-4" data-testid="results-title">
                Verification Results
              </h1>
              <div className="flex flex-wrap gap-4 text-sm font-mono text-slate-600">
                <span data-testid="detected-language">Language: <strong>{results.detected_language}</strong></span>
                <span data-testid="claims-count">Claims Analyzed: <strong>{results.claims.length}</strong></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Overall Assessment */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="bg-gradient-to-br from-blue-900 to-blue-800 text-white p-8 md:p-12 rounded-xl shadow-lg mb-12"
          data-testid="overall-assessment"
        >
          <div className="flex items-start gap-4 mb-4">
            <Shield className="w-8 h-8 flex-shrink-0 mt-1" />
            <div>
              <h2 className="font-serif font-bold text-2xl md:text-3xl mb-4">Overall Assessment</h2>
              <p className="text-lg md:text-xl text-blue-100 leading-relaxed">
                {results.overall_assessment}
              </p>
            </div>
          </div>
        </motion.div>

        {/* Original Text Preview */}
        {results.original_text && (
          <div className="bg-white p-6 rounded-lg border border-slate-200 mb-12" data-testid="original-text">
            <h3 className="font-sans font-semibold text-lg mb-3 uppercase text-slate-700">Original Content</h3>
            <p className="text-slate-600 leading-relaxed font-mono text-sm">
              {results.original_text}
            </p>
          </div>
        )}

        {/* Claims Results */}
        <div className="space-y-8">
          <h2 className="font-serif font-bold text-3xl mb-6">Claim-by-Claim Analysis</h2>
          
          {results.claims.map((claim, index) => (
            <motion.div
              key={claim.claim_id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow"
              data-testid={`claim-card-${index}`}
            >
              {/* Claim Header */}
              <div className="p-6 md:p-8 border-b border-slate-100">
                <div className="flex items-start gap-6">
                  <div className={`verdict-stamp p-4 rounded-lg border-2 ${getVerdictStyles(claim.verdict)}`}>
                    {getVerdictIcon(claim.verdict)}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <span
                        data-testid={`claim-verdict-${index}`}
                        className={`font-serif font-black italic tracking-tighter uppercase text-2xl ${getVerdictStyles(claim.verdict)}`}
                      >
                        {claim.verdict}
                      </span>
                      <span className="font-mono text-xs text-slate-500">Claim #{index + 1}</span>
                    </div>
                    
                    <p className="text-lg text-slate-700 leading-relaxed mb-4" data-testid={`claim-text-${index}`}>
                      "{claim.claim_text}"
                    </p>
                    
                    {/* Confidence Score */}
                    <div className="space-y-2" data-testid={`claim-confidence-${index}`}>
                      <div className="flex justify-between text-sm font-mono">
                        <span className="text-slate-600">Confidence Score</span>
                        <span className="font-bold">{Math.round(claim.confidence)}%</span>
                      </div>
                      <div className="relative h-2 bg-slate-100 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${claim.confidence}%` }}
                          transition={{ duration: 1, delay: 0.3 }}
                          className={`h-full ${getConfidenceColor(claim.confidence)} rounded-full`}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Explanation */}
              <div className="p-6 md:p-8 bg-slate-50">
                <h4 className="font-sans font-semibold text-sm uppercase tracking-wider text-slate-600 mb-3">
                  Explanation
                </h4>
                <p className="text-slate-700 leading-relaxed" data-testid={`claim-explanation-${index}`}>
                  {claim.explanation}
                </p>
              </div>

              {/* Supporting Sources */}
              {claim.supporting_sources && claim.supporting_sources.length > 0 && (
                <div className="p-6 md:p-8 border-t border-slate-200">
                  <h4 className="font-sans font-semibold text-sm uppercase tracking-wider text-emerald-700 mb-4">
                    Supporting Evidence ({claim.supporting_sources.length})
                  </h4>
                  <div className="space-y-3">
                    {claim.supporting_sources.map((source, sourceIndex) => (
                      <div
                        key={sourceIndex}
                        className="flex items-start gap-3 p-3 bg-emerald-50 rounded-lg border border-emerald-100"
                        data-testid={`supporting-source-${index}-${sourceIndex}`}
                      >
                        <Shield className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-semibold text-sm text-emerald-900">
                              {source.source_name}
                            </span>
                            <span className="text-xs font-mono text-emerald-700">
                              {source.credibility_score}% credible
                            </span>
                          </div>
                          <p className="text-sm text-emerald-800 mb-2">{source.relevant_text}</p>
                          {source.source_url && (
                            <a
                              href={source.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-xs text-emerald-600 hover:text-emerald-700 font-medium"
                            >
                              View Source <ExternalLink className="w-3 h-3" />
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Contradicting Sources */}
              {claim.contradicting_sources && claim.contradicting_sources.length > 0 && (
                <div className="p-6 md:p-8 border-t border-slate-200">
                  <h4 className="font-sans font-semibold text-sm uppercase tracking-wider text-rose-700 mb-4">
                    Contradicting Evidence ({claim.contradicting_sources.length})
                  </h4>
                  <div className="space-y-3">
                    {claim.contradicting_sources.map((source, sourceIndex) => (
                      <div
                        key={sourceIndex}
                        className="flex items-start gap-3 p-3 bg-rose-50 rounded-lg border border-rose-100"
                        data-testid={`contradicting-source-${index}-${sourceIndex}`}
                      >
                        <Shield className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-semibold text-sm text-rose-900">
                              {source.source_name}
                            </span>
                            <span className="text-xs font-mono text-rose-700">
                              {source.credibility_score}% credible
                            </span>
                          </div>
                          <p className="text-sm text-rose-800 mb-2">{source.relevant_text}</p>
                          {source.source_url && (
                            <a
                              href={source.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-xs text-rose-600 hover:text-rose-700 font-medium"
                            >
                              View Source <ExternalLink className="w-3 h-3" />
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="mt-12 flex justify-center">
          <Button
            data-testid="verify-another-button"
            onClick={onBack}
            className="bg-blue-900 text-white hover:bg-blue-800 rounded-none px-8 py-4 text-lg font-bold tracking-wide shadow-lg hover:-translate-y-0.5 transition-all"
          >
            Verify Another Content
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
