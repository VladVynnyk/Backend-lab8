// src/components/DeleteButton.tsx
import React from 'react';

type DeleteButtonProps = {
  entityName: string;
  id: number;
  onDeleteSuccess: () => void;
};

const DeleteButton: React.FC<DeleteButtonProps> = ({ entityName, id, onDeleteSuccess }) => {
  const handleDelete = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/${entityName}/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        onDeleteSuccess(); // Викликається при успішному видаленні
      } else {
        console.error("Error deleting item:", await response.json());
      }
    } catch (error) {
      console.error("Error deleting item:", error);
    }
  };

  return (
    <button
      onClick={handleDelete}
      className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-700 focus:outline-none"
    >
      Delete
    </button>
  );
};

export default DeleteButton;
