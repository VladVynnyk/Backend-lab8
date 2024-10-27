// src/components/EntityTable.tsx
import React, { useState, useEffect } from 'react';
import {
  useGetCategoriessQuery,
  useGetUsersQuery,
  useGetPropertiesQuery,
  useGetThermometersQuery,
} from "../../store/api/tableApi";
import NoData from "./NoData";
import EntityForm from "../Form/EntityForm.tsx";
import DeleteButton from "../Button/DeleteButton.tsx";
import { transformThermometersData } from "../../utils/utils";

const DataTable: React.FC = () => {
  const [currentEntity, setCurrentEntity] = useState<'thermometers' | 'users' | 'categories' | 'properties'>('thermometers');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingData, setEditingData] = useState<{ [key: string]: any } | null>(null);
  const [dataUpdated, setDataUpdated] = useState(false);

  // Запити до API з повторним запитом при зміні `dataUpdated`
  const { data: thermometersData, refetch: refetchThermometers } = useGetThermometersQuery();
  const { data: usersData, refetch: refetchUsers } = useGetUsersQuery();
  const { data: categoriesData, refetch: refetchCategories } = useGetCategoriessQuery();
  const { data: propertiesData, refetch: refetchProperties } = useGetPropertiesQuery();

  useEffect(() => {
    if (dataUpdated) {
      switch (currentEntity) {
        case 'thermometers':
          refetchThermometers();
          break;
        case 'users':
          refetchUsers();
          break;
        case 'categories':
          refetchCategories();
          break;
        case 'properties':
          refetchProperties();
          break;
        default:
          break;
      }
      setDataUpdated(false);
    }
  }, [dataUpdated, currentEntity, refetchThermometers, refetchUsers, refetchCategories, refetchProperties]);
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  //@ts-expect-error
  let data;
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  //@ts-expect-error
  let fields;
  switch (currentEntity) {
    case 'thermometers':
      data = thermometersData;
      fields = [
        { name: 'name', label: 'Thermometer Name', type: 'text' },
        { name: 'vendor', label: 'Vendor', type: 'text' },
        { name: 'category', label: 'Category', type: 'select' },
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

  //eslint-disable-next-line @typescript-eslint/ban-ts-comment
  //@ts-expect-error
  const transformedData = currentEntity === 'thermometers' && data ? transformThermometersData(data) : data;


  const openForm = (itemData: { [key: string]: any } | null = null) => {
    setEditingData(itemData);
    setIsFormOpen(true);
  };

  const closeForm = () => {
    setEditingData(null);
    setIsFormOpen(false);
  };

  const handleFormSubmitSuccess = () => {
    setDataUpdated(true);
    closeForm();
  };

  const handleDeleteSuccess = () => {
    setDataUpdated(true);
  };

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
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            //@ts-expect-error
          fields={fields}
          initialValues={editingData || {}}
          onSubmitSuccess={handleFormSubmitSuccess}
          onCancel={closeForm}
          entityName={currentEntity}
          id={editingData ? editingData.id : undefined}
          buttonText={editingData ? "Update" : "Add"}
        />
      ) : (
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {/*eslint-disable-next-line @typescript-eslint/ban-ts-comment*/}
              {/*@ts-expect-error*/}
              {transformedData.length > 0 && Object.keys(transformedData[0]).map((key) => (
                <th key={key} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {key}
                </th>
              ))}
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {/*eslint-disable-next-line @typescript-eslint/ban-ts-comment*/}
            {/*@ts-expect-error*/}
            {transformedData.map((item: any) => (
              <tr key={item.id} className="hover:bg-gray-100">
                {Object.values(item).map((value, index) => (
                  <td key={index} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {/*eslint-disable-next-line @typescript-eslint/ban-ts-comment*/}
                    {/*@ts-expect-error*/}
                    {value}
                  </td>
                ))}
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 flex space-x-2">
                  <button
                    onClick={() => openForm(item)}
                    className="mr-2 px-4 py-2 bg-yellow-500 text-white rounded"
                  >
                    Edit
                  </button>
                  <DeleteButton
                    entityName={currentEntity}
                    id={item.id}
                    onDeleteSuccess={handleDeleteSuccess}
                  />
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
