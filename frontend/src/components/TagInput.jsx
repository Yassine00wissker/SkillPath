import { X } from 'lucide-react';
import { useState } from 'react';

export default function TagInput({ label, tags = [], onChange }) {
    const [input, setInput] = useState('');

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && input.trim()) {
            e.preventDefault();
            if (!tags.includes(input.trim())) {
                onChange([...tags, input.trim()]);
            }
            setInput('');
        }
    };

    const removeTag = (tagToRemove) => {
        onChange(tags.filter(tag => tag !== tagToRemove));
    };

    return (
        <div>
            <label className="block text-sm font-medium text-muted mb-2">{label}</label>
            <div className="flex flex-wrap gap-2 mb-2 p-1 min-h-[32px]">
                {tags.map(tag => (
                    <span key={tag} className="bg-primary/10 text-primary px-2 py-1 rounded-md text-sm flex items-center gap-1">
                        {tag}
                        <button type="button" onClick={() => removeTag(tag)} className="hover:text-white">
                            <X className="w-3 h-3" />
                        </button>
                    </span>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                className="w-full bg-background border border-white/10 rounded-lg py-2 px-4 text-white focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
                placeholder="Type and press Enter..."
            />
        </div>
    );
}
