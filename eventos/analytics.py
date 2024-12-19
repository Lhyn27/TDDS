import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from .models import Event, OrderItem, Category
from django.db.models import Count, Sum, F
from django.utils import timezone
import io
import base64

class EventAnalytics:
    @staticmethod
    def generate_event_analysis():
        # Obtener todas las categorías de la base de datos
        all_categories = Category.objects.values_list('name', flat=True)
        
        # Obtener datos de ventas
        sales_data = OrderItem.objects.values(
            'event__name', 
            'event__category__name'
        ).annotate(
            total_tickets=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('price'))
        ).order_by('-total_tickets')

        # Crear DataFrame
        df = pd.DataFrame(sales_data)
        
        # Crear archivo Excel con todas las categorías
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Hoja de eventos más vendidos
            df.to_excel(writer, sheet_name='Eventos más vendidos', index=False)
            
            # Preparar análisis por categoría incluyendo todas las categorías
            category_data = {cat: 0 for cat in all_categories}
            for cat, tickets in df.groupby('event__category__name')['total_tickets'].sum().items():
                if cat in category_data:
                    category_data[cat] = tickets
            
            category_df_excel = pd.DataFrame([
                {'Categoría': cat, 'Total Tickets': tickets, 'Porcentaje': 0}
                for cat, tickets in category_data.items()
            ])
            
            # Calcular porcentajes para Excel
            total_tickets = category_df_excel['Total Tickets'].sum()
            if total_tickets > 0:
                category_df_excel['Porcentaje'] = (category_df_excel['Total Tickets'] / total_tickets) * 100
            
            category_df_excel.to_excel(writer, sheet_name='Análisis por categoría', index=False)

        # Para el gráfico de torta, usar solo las categorías con ventas
        category_df_graph = df.groupby('event__category__name')['total_tickets'].sum().reset_index()
        category_df_graph.columns = ['Categoría', 'Total Tickets']
        category_df_graph = category_df_graph.sort_values('Total Tickets', ascending=False)

        # Calcular porcentajes para el gráfico
        total_tickets_graph = category_df_graph['Total Tickets'].sum()
        if total_tickets_graph > 0:
            category_df_graph['Porcentaje'] = (category_df_graph['Total Tickets'] / total_tickets_graph) * 100

        # Crear figura con dos subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Gráfico de barras - Top eventos
        sns.barplot(data=df.head(10), x='event__name', y='total_tickets', ax=ax1)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=20, ha='right')
        ax1.set_title('Top Eventos más Vendidos')

        # Si hay más de 6 categorías, agrupar las menos vendidas
        if len(category_df_graph) > 5:
            top_categories = category_df_graph.head(5)
            others = pd.DataFrame([{
                'Categoría': 'Otras categorías',
                'Total Tickets': category_df_graph.iloc[5:]['Total Tickets'].sum(),
                'Porcentaje': category_df_graph.iloc[5:]['Porcentaje'].sum()
            }])
            category_df_graph = pd.concat([top_categories, others])

        # Crear gráfico de torta
        wedges, texts, autotexts = ax2.pie(
            category_df_graph['Total Tickets'],
            labels=category_df_graph['Categoría'],
            autopct='%1.1f%%',
            pctdistance=0.85
        )
        
        plt.setp(autotexts, size=8)
        plt.setp(texts, size=8)
        
        ax2.set_title('Distribución de Ventas por Categoría')

        plt.tight_layout()
        
        # Guardar gráficos en memoria
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=300)
        img_buffer.seek(0)
        graph = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return output.getvalue(), graph