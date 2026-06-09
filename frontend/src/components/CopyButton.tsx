import { Check, Copy } from 'lucide-react';
import { useState } from 'react';

type CopyButtonProps = {
  value: string;
  label: string;
};

export function CopyButton({ value, label }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(value);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1400);
  }

  return (
    <button className="icon-button" type="button" onClick={handleCopy} title={label} aria-label={label}>
      {copied ? <Check size={16} /> : <Copy size={16} />}
    </button>
  );
}

