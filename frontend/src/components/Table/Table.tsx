// src/components/EntityTable.tsx
import React, { useState } from 'react';
import {
  useGetCategoriessQuery,
  useGetUsersQuery,
  useGetPropertiesQuery,
  useGetThermometersQuery,
} from "../../store/api/tableApi";
import NoData from "./NoData";
import EntityForm from "../Form/EntityForm.tsx";
import { transformThermometersData } from "../../utils/utils";

const DataTable: React.FC = () => {
  const [currentEntity, setCurrentEntity] = useState<'thermometers' | 'users' | 'categories' | 'properties'>('thermometers');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingData, setEditingData] = useState<{ [key: string]: any } | null>(null);

  // Запити до API
  const { data: thermometersData, error: thermometersError, isLoading: isLoadingThermometers } = useGetThermometersQuery();
  const { data: usersData, error: usersError } = useGetUsersQuery();
  const { data: categoriesData, error: categoriesError } = useGetCategoriessQuery();
  const { data: propertiesData, error: propertiesError } = useGetPropertiesQuery();

  // Визначення даних відповідно до вибраної сутності
  let data;
  let fields;
  switch (currentEntity) {
    case 'thermometers':
      data = thermometersData;
      fields = [
        { name: 'name', label: 'Thermometer Name', type: 'text' },
        { name: 'vendor', label: 'Vendor', type: 'text' },
        { name: 'min_temp', label: 'Minimum Temperature', type: 'number' },
        { name: 'max_temp', label: 'Maximum Temperature', type: 'number' },
        { name: 'accuracy', label: 'Accuracy', type: 'number' },
      ];
      break;
    case 'users':
      data = usersData;
      fields = [
        { name: 'username', label: 'Username', type: 'text' },
        { name: 'password', label: 'Password', type: 'password' },
      ];
      break;
    case 'categories':
      data = categoriesData;
      fields = [
        { name: 'name', label: 'Category Name', type: 'text' },
      ];
      break;
    case 'properties':
      data = propertiesData;
      fields = [
        { name: 'name', label: 'Property Name', type: 'text' },
        { name: 'units', label: 'Units', type: 'text' },
      ];
      break;
    default:
      data = [];
      fields = [];
  }

  // Трансформація даних для термометрів
  const transformedData = currentEntity === 'thermometers' && data ? transformThermometersData(data) : data;

  // Функція для відкриття форми
  const openForm = (itemData: { [key: string]: any } | null = null) => {
    setEditingData(itemData);
    setIsFormOpen(true);
  };

  // Функція для закриття форми
  const closeForm = () => {
    setEditingData(null);
    setIsFormOpen(false);
  };

  // Функція для обробки відправки форми
  const handleFormSubmit = (formData: { [key: string]: any }) => {
    console.log("Submitted data:", formData);
    // Тут можна додати API виклик для оновлення або додавання даних
    closeForm();
  };

  // Обробка станів
  if (isLoadingThermometers) return <div>Loading Thermometers...</div>;
  if (currentEntity === 'thermometers' && thermometersError) return <div>Error loading thermometers: {thermometersError.message}</div>;
  if (currentEntity === 'users' && usersError) return <div>Error loading users: {usersError.message}</div>;
  if (currentEntity === 'categories' && categoriesError) return <div>Error loading categories: {categoriesError.message}</div>;
  if (currentEntity === 'properties' && propertiesError) return <div>Error loading properties: {propertiesError.message}</div>;

  if (!data || data.length === 0) return <NoData />;

  return (
    <div className="container mx-auto p-4">
      <div className="mb-4">
        <button onClick={() => setCurrentEntity('thermometers')} className="mr-2 px-4 py-2 bg-blue-500 text-white rounded">
          Thermometers
        </button>
        <button onClick={() => setCurrentEntity('users')} className="mr-2 px-4 py-2 bg-blue-500 text-white rounded">
          Users
        </button>
        <button onClick={() => setCurrentEntity('categories')} className="mr-2 px-4 py-2 bg-blue-500 text-white rounded">
          Categories
        </button>
        <button onClick={() => setCurrentEntity('properties')} className="mr-2 px-4 py-2 bg-blue-500 text-white rounded">
          Properties
        </button>
        <button onClick={() => openForm()} className="px-4 py-2 bg-green-500 text-white rounded">
          Add New {currentEntity.charAt(0).toUpperCase() + currentEntity.slice(1)}
        </button>
      </div>

      {isFormOpen ? (
        <EntityForm
          fields={fields}
          initialValues={editingData || {}}
          onSubmit={handleFormSubmit}
          buttonText={editingData ? "Update" : "Add"}
        >
          <button
            type="button"
            onClick={closeForm}
            className="w-full mt-4 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
          >
            Cancel
          </button>
        </EntityForm>
      ) : (
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {transformedData.length > 0 && Object.keys(transformedData[0]).map((key) => (
                <th key={key} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {key}
                </th>
              ))}
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transformedData.map((item: any) => (
              <tr key={item.id} className="hover:bg-gray-100">
                {Object.values(item).map((value, index) => (
                  <td key={index} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {value}
                  </td>
                ))}
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <button
                    onClick={() => openForm(item)}
                    className="mr-2 px-4 py-2 bg-yellow-500 text-white rounded"
                  >
                    Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default DataTable;
