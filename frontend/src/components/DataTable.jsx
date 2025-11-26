import { Edit, Trash2 } from 'lucide-react';

export default function DataTable({ columns, data, onEdit, onDelete }) {
    return (
        <div className="overflow-x-auto rounded-lg border border-white/10">
            <table className="w-full text-left text-sm text-muted">
                <thead className="bg-surface text-white uppercase tracking-wider">
                    <tr>
                        {columns.map((col) => (
                            <th key={col.key} className="px-6 py-4 font-medium">
                                {col.label}
                            </th>
                        ))}
                        <th className="px-6 py-4 text-right">Actions</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-white/5 bg-background">
                    {data.map((row) => (
                        <tr key={row.id} className="hover:bg-white/5 transition-colors">
                            {columns.map((col) => (
                                <td key={col.key} className="px-6 py-4 whitespace-nowrap">
                                    {col.render ? col.render(row[col.key], row) : row[col.key]}
                                </td>
                            ))}
                            <td className="px-6 py-4 text-right flex justify-end gap-2">
                                <button
                                    onClick={() => onEdit(row)}
                                    className="p-2 text-primary hover:bg-primary/10 rounded-lg transition-colors"
                                >
                                    <Edit className="w-4 h-4" />
                                </button>
                                <button
                                    onClick={() => onDelete(row)}
                                    className="p-2 text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                                >
                                    <Trash2 className="w-4 h-4" />
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
